
def bootstrap(element):
    import toga
    parts = element.dataset.togaClass.split('.')
    bootstrap_method = getattr(toga, 'bootstrap_' + parts[1])
    result = bootstrap_method(element)
    return result
