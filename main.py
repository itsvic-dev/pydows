from fluent.views.notification import Notification

if __name__ == "__main__":
    notification = Notification(
        header=("omame.png", "omame"),
        body="well this is weird",
    )
    notification.paint().show()
