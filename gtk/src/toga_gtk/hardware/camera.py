from __future__ import annotations

import asyncio

from toga_gtk.libs import FeatureRequiresMissingDependency, Gio, GLib, Gst, Wp


class CameraDevice:
    pass


class Camera:
    def __init__(self, interface):
        if Gst is None:
            # CI (where coverage is enforced) must always have GStreamer available
            # in order to perform the rest of the tests
            raise FeatureRequiresMissingDependency(
                "camera", "GStreamer", "hardware/camera.html#system-requirements"
            )  # pragma: no cover

        if Wp is None:
            # CI (where coverage is enforced) must always have WirePlumber available
            # in order to perform the rest of the tests
            raise FeatureRequiresMissingDependency(
                "camera", "WirePlumber", "hardware/camera.html#system-requirements"
            )  # pragma: no cover

        Gst.init(None)
        Wp.init(Wp.InitFlags.PIPEWIRE)

        self.interface = interface

        self.permission_result: None | bool = None

    _handle_token_count = 0

    def _get_handle_token(self):
        self._handle_token_count += 1
        return str(self._handle_token_count)

    def has_permission(self):
        return bool(self.permission_result)

    def _create_portal_proxy(self) -> asyncio.Future[Gio.DBusProxy]:
        future = asyncio.Future()

        def finish(_, task, *__):
            try:
                portal_proxy = Gio.DBusProxy.new_for_bus_finish(task)
            except Exception as e:
                future.set_exception(e)
            else:
                future.set_result(portal_proxy)

        Gio.DBusProxy.new_for_bus(
            bus_type=Gio.BusType.SESSION,
            flags=Gio.DBusProxyFlags.NONE,
            info=None,
            name="org.freedesktop.portal.Desktop",
            object_path="/org/freedesktop/portal/desktop",
            interface_name="org.freedesktop.portal.Camera",
            cancellable=None,
            callback=finish,
            user_data=None,
        )

        return future

    def _subscribe_to_access_response(
        self, connection, request_path
    ) -> asyncio.Future[bool]:
        future = asyncio.Future()

        def callback(
            connection,
            sender_name,
            object_path,
            interface_name,
            signal_name,
            parameters,
            *user_data,
        ):
            # parameters will be "(ua{sv})", i.e., a tuple[int, dict]
            unwrapped_response = parameters.get_child_value(0).get_uint32()
            future.set_result(unwrapped_response)

        connection.signal_subscribe(
            sender="org.freedesktop.portal.Desktop",
            interface_name="org.freedesktop.portal.Request",
            member="Response",
            object_path=request_path,
            arg0=None,
            flags=Gio.DBusSignalFlags.NONE,
            callback=callback,
            user_data=None,
        )

        return future

    def _get_access_camera_request_handle(self, connection) -> tuple[str, str]:
        name = connection.get_unique_name()[1:].replace(".", "_")
        token = f"access_camera_{self._get_handle_token()}"

        path = f"/org/freedesktop/portal/desktop/request/{name}/{token}"

        return path, token

    def _access_camera(self, portal, handle_token) -> asyncio.Future[str]:
        future = asyncio.Future()

        def result_handler(_, result, *__):
            if isinstance(result, Exception):
                future.set_exception(result)
            else:
                future.set_result(result)

        portal.AccessCamera(
            "(a{sv})",
            {"handle_token": GLib.Variant("s", handle_token)},
            result_handler=result_handler,
        )

        return future

    async def _request_permission(self, future):
        try:
            self.portal = await self._get_portal_proxy()
            connection = self.portal.get_connection()
            request_path, handle_token = self._get_access_camera_request_handle(
                connection
            )

            # Subscribe _before_ sending the request to prevent possibility of race
            # conditions. See docs (linked below) for further details about proper
            # handling of the portal ``Request``/``Response`` cycle
            # https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Request.html#description
            access_response_future = self._subscribe_to_access_response(
                connection, request_path
            )

            actual_path = await self._access_camera(self.portal, handle_token)
            # XDG implementations < 0.9 will not use the standard request path.
            # As such, if the actual path returned by AccessCamera differs from
            # the one created above, then a new response subscription is needed and
            # the potential race condition cannot be avoided.
            # See XDG Request docs linked above for further details on this quirk
            if actual_path != request_path:
                access_response_future = self._subscribe_to_access_response(
                    connection, actual_path
                )

            access_response = await access_response_future

            # https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Request.html#org-freedesktop-portal-request-response
            # 0 -> user allowed camera access
            # 1 -> user denied access
            # 2 -> something else happened (but not approval)
            self.permission_result = access_response == 0
        except Exception as e:
            future.set_exception(e)
        else:
            # if self.permission_result:
            #     await self._populate_devices()

            future.set_result(self.permission_result)

    def request_permission(self, future):
        asyncio.create_task(self._request_permission(future))

    def _get_glib_main_context(self):
        loop = asyncio.get_running_loop()
        breakpoint()
        return loop._context

    # async def _populate_devices(self):
    #     fd = await self._open_pipe_wire_remote()
    #     main_context = self._get_glib_main_context()

    #     self.wp_obj_manager = Wp.ObjectManager.new()
    #     self.wp_core = Wp.Core.new(main_context, None, None)
    #     self.wp_core.connect()

    def _open_pipe_wire_remote(self) -> asyncio.Future[GLib.DBus]:
        future = asyncio.Future()

        def result_handler(_, result, *__):
            if isinstance(result, Exception):
                future.set_exception(result)
            else:
                future.set_result(result)

        self.portal.OpenPipeWireRemote(
            "(a{sv})",
            {},
            result_handler=result_handler,
        )

        return future

    def get_devices(self):
        if not (self.has_permission and self.portal):
            # cannot list devices without permission or if the portal is not initialised
            return []
