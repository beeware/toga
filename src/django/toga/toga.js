require('bootstrap/scss/bootstrap.scss');
require('font-awesome/scss/font-awesome.scss');


var batavia = require('@pybee/batavia');

window.toga = {
    handler: function(ref, widget) {
        if (ref === "None") {
            return function() {
                console.log("No handler defined for " + ref + " on " + widget);
            };
        } else {
            var context;
            var name;

            if (ref[0] === "(") {
                var parts = ref.slice(1,-1).split(',');
                context = document.getElementById(parts[0]).toga;
                name = parts[1];
                return function(widget) {
                    return function(evt) {
                        var globals = new batavia.core.Dict({
                            '__builtins__': batavia.builtins,
                            '__name__': '__main__',
                            '__doc__': null,
                            '__package__': null,
                        });
                        var locals = new batavia.core.Dict({
                            // '__builtins__': batavia.builtins,
                            '__name__': '__main__??',
                            '__doc__': null,
                            '__package__': null,
                            'self': context
                        });
                        window.toga.vm.run_method(name, [context, widget], null, locals, globals);
                    };
                }(widget);
            } else {
                return function(evt) {
                    window.toga.vm.run_method(ref, [widget], null);
                };
            }
        }
    },

    post: function(url, payload) {
        $.ajax({
            'url': url,
            'type': 'post',
            'data': payload,
        });
    },

    delete: function(url) {
        $.ajax({
            'url': url,
            'type': 'delete'
        });
    },

    // Define a stdout and stderr function that will output to the page.
    PyConsole: function() {
        function PyConsole(element) {
            this.element = element;
        }

        PyConsole.prototype.write = function(args, kwargs) {
            var text = document.createTextNode(args[0]);
            this.element.appendChild(text);
        }

        PyConsole.prototype.flush = function(args, kwargs) {}

        return PyConsole;
    }(),

    PyErrConsole: function() {
        function PyErrConsole(element) {
            this.element = element
        }

        PyErrConsole.prototype.write = function(args, kwargs) {
            var err = document.createElement('span');
            err.className = "error";
            var text = document.createTextNode(args[0])

            err.appendChild(text)
            this.element.appendChild(err);
        }

        PyErrConsole.prototype.flush = function(args, kwargs) {}

        return PyErrConsole;
    }()
};


window.onload = function() {
    console.log('Create VM...');
    // If there is a console element on the page, use it
    var toga_console = document.getElementById('toga-console');
    var config;
    if (toga_console !== null) {
        config = {
            'stdout': new window.toga.PyConsole(toga_console),
            'stderr': new window.toga.PyErrConsole(toga_console),
        }
    } else {
        config = {};
    }
    window.toga.vm = new batavia.VirtualMachine(config);

    console.log('Instantiate Toga objects...');
    var widgets = document.querySelectorAll('[data-toga-class]');
    var w;
    // Create widgets
    for (w = 0; w < widgets.length; w++) {
        console.log("Create " + widgets[w].dataset.togaClass + ':' + widgets[w].id);
        window.toga.vm.run_method('bootstrap', [widgets[w]]);
    }
    // Add child relationships
    for (w = 0; w < widgets.length; w++) {
        if (widgets[w].toga.children) {
            var children = document.querySelectorAll("[data-toga-parent='" + widgets[w].id + "']");
            console.log("Add children for " + widgets[w].dataset.togaClass + ':' + widgets[w].id);
            for (var c = 0; c < children.length; c++) {
                console.log("    Add child " + children[c].dataset.togaClass + ':' + children[c].id);
                widgets[w].toga.add_child.__call__.call(
                    window.toga.vm,
                    new batavia.types.List([widgets[w].toga, children[c].toga]),
                    new batavia.types.JSDict(),
                    null
                );
            }
        // } else {
        //     console.log("Non-child widget - " + widgets[w].dataset.togaClass + ':' + widgets[w].id);
        }
    }
    // Hook up ports
    // for (w = 0; w < widgets.length; w++) {
    //     console.log("Set ports for " + widgets[w].dataset.togaClass + ":" + widgets[w].toga.id);
    //     var ports = widgets[w].dataset.togaPorts.split(',');
    //     for (var port = 0; port < ports.length; port++) {
    //         var parts = ports[port].split('=');
    //         if (parts.length == 2 && parts[0] !== 'parent') {
    //             widgets[w].toga.ports[parts[0]] = parts[1];
    //             widgets[w].toga[parts[0]] = document.getElementById(parts[1]).toga;
    //         }
    //     }
    // }
    console.log('Toga is ready.');
};
