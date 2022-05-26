START_TEXT = """
Hi!

Once you start testing I will update you when you want ⏱
When a failure occurs I will notify you immediately 🖨️

The steps to *start* bot: 🏁
--------------------------------------------------------
• ***Set up path*** - gives bot your path to pytest folder 🌐

• ***Edit notifications period*** - every _<input>_ seconds get response _(600 by default)_ ♾️

• ***Edit fails period*** - every _<input>_ seconds get messages if tests failed _(30 by default)_ 🔁

• ***Start testing*** - start checking tests & getting updates 📺
"""

HELP_TEXT = """
The steps to start bot: 🏁
--------------------------------------------------------
• ***Set up path*** - gives bot your path to pytest folder 🌐

• ***Edit notifications period*** - every _<input>_ seconds get response _(600 by default)_ ♾️

• ***Edit fails period*** - every _<input>_ seconds get messages if tests failed _(30 by default)_ 🔁

• ***Start testing*** - start checking tests & getting updates 📺
--------------------------------------------------------


Commands inside ***Start testing***:
--------------------------------------------------------
• ***Unmute failures notifications*** - unmutes failures detection if muted _(unmuted by default)_ 🔊

• ***Mute failures notifications*** - mutes failures detection if not muted 🔇

• ***Get only scheduled notifications*** - turn off alert failures updates 📅

• ***Get all notifications*** - get all updates _(all by default)_ 🔔

• ***Stop testing*** - stop getting updates 🎬
--------------------------------------------------------

Enjoy 🍿
    """

SET_UP_PATH = 'To set the path click one of the buttons below🔽'
SETTING_PATH_INSTRUCTION = 'Input the path to your pytest folder: '
INVALID_PATH = 'Path is invalid...'
SETTING_PATH_SUCCESS = 'Path successfully set.'

START_TESTING_INSTRUCTION_1 = 'Testing starting...'
START_TESTING_INSTRUCTION_2 = 'Now you will get periodical notifications and messages about tests failure if it occurs!'
START_TESTING_INSTRUCTION_3 = 'To modify the process click one of the buttons below🔽'

STOP_TESTING = 'Testing is being stopped...'

GET_ALL_NOTIFICATIONS_ANSWER = 'Now you will also receive notifications about failures...'
GET_SCHEDULED_NOTIFICATIONS_ANSWER = 'Now you will only receive scheduled notifications...'
LOUD_FAILURE_NOTIFICATIONS = 'Now failure notifications are loud...'
MUTED_FAILURE_NOTIFICATIONS = 'Now failure notifications are muted...'
UPDATE_PERIOD_FAILURE = 'Chosen period is not updated. Please, read the instruction...'
UPDATE_PERIOD_SUCCESS = 'Chosen period was successfully updated.'

NOTIFICATION_PERIOD_INSTRUCTION_1 = 'Every N seconds you will get the notification independently on tests result\nInput N: '
NOTIFICATION_PERIOD_INSTRUCTION_2 = 'Provide the information in form: "Notification {your_seconds}"'

FAILURE_PERIOD_INSTRUCTION_1 = 'Once you get failure notification, you will get it every K seconds\nInput K: '
FAILURE_PERIOD_INSTRUCTION_2 = 'Provide the information in form: "Failure {your_seconds}"'

COMMAND_START = 'start'
BUTTON_HELP = 'Help'
BUTTON_SET_PATH = 'Set up path'
BUTTON_RESET_PATH = 'Reset path'
BUTTON_START_TESTING = 'Start testing'
BUTTON_END_TESTING = 'End testing'
BUTTON_EDIT_FAILURE_PERIOD = 'Edit failure period'
BUTTON_EDIT_NOTIFICATIONS_PERIOD = 'Edit notifications period'
BUTTON_MUTE_FAILURE_NOTIFICATIONS = 'Mute failure notifications'
BUTTON_UNMUTE_FAILURE_NOTIFICATIONS = 'Unmute failure notifications'
BUTTON_GET_ONLY_SCHEDULED_NOTIFICATIONS = 'Get only scheduled notifications'
BUTTON_GET_ALL_NOTIFICATIONS = 'Get all notifications'

CHANGE_NOTIFICATION_PERIOD = 'Notification'
CHANGE_FAILURE_PERIOD = 'Failure'
