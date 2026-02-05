from pyscript import web, when


@when("click", "#my-button")
def handler():
    output_div = web.page["output"]
    output_div.innerText = "Button clicked!"
