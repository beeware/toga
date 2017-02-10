'''
# This script builds a table to show the supported platforms for Toga and the components that are supported
'''
import inspect

"""
A dictionary of components, index is the module name and value is the class name
"""
COMPONENT_LIST = {}

"""
Static list of potential platforms, index is the directory and value is the friendly name
"""
PLATFORM_LIST = {
    'android': 'Android',
    'cocoa': 'Mac OS cocoa',
    'core': 
}