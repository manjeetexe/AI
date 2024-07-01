import AppKit

def display_alert(title, message):
    alert = AppKit.NSAlert.alloc().init()
    alert.setMessageText_(title)
    alert.setInformativeText_(message)
    alert.addButtonWithTitle_("OK")
    alert.runModal()

display_alert("Test Alert", "This is a test alert message.")

