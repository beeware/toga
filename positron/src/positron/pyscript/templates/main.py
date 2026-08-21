from reflected import server, window

button = window.document.getElementById("my-button")
output = window.document.getElementById("output")


async def handler(event):
    output.append("Hello World in the app")
    server.builtins.print("Hello World on the server")


button.addEventListener("click", handler)
