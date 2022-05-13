from datetime import datetime, timedelta
import win32com.client

# SEMPRE CRIA A TAREFA E SUBSTITUI SE ELA JA EXISTE
TASK_CREATE_OR_UPDATE = 6

# NUNCA NECESSITA DE LOGIN PARA ALTERAR
TASK_LOGON_NONE = 0

# TASK_TRIGGER_TYPE
TASK_TRIGGER_EVENT = 0
TASK_TRIGGER_TIME = 1
TASK_TRIGGER_DAILY = 2
TASK_TRIGGER_WEEKLY = 3
TASK_TRIGGER_MONTHLY = 4
TASK_TRIGGER_MONTHLYDOW = 5
TASK_TRIGGER_IDLE = 6
TASK_TRIGGER_REGISTRATION = 7
TASK_TRIGGER_BOOT = 8
TASK_TRIGGER_LOGON = 9
TASK_TRIGGER_SESSION_STATE_CHANGE = 11

# DICIONARIO COM OS TIPOS DE TRIGGER
trigger_types = {
    "Event": TASK_TRIGGER_EVENT,
    "Once": TASK_TRIGGER_TIME,
    "Daily": TASK_TRIGGER_DAILY,
    "Weekly": TASK_TRIGGER_WEEKLY,
    "Monthly": TASK_TRIGGER_MONTHLY,
    "MonthlyDay": TASK_TRIGGER_MONTHLYDOW,
    "OnTaskCreation": TASK_TRIGGER_REGISTRATION
}

scheduler = win32com.client.Dispatch('Schedule.Service')
scheduler.connect()

def _get_date_time_format(dt_string):
    """
    Copied from win_system.py (_get_date_time_format)

    Function that detects the date/time format for the string passed.

    :param str dt_string:
        A date/time string

    :return: The format of the passed dt_string
    :rtype: str
    """
    valid_formats = [
        "%I:%M:%S %p",
        "%I:%M %p",
        "%H:%M:%S",
        "%H:%M",
        "%Y-%m-%d",
        "%m-%d-%y",
        "%m-%d-%Y",
        "%m/%d/%y",
        "%m/%d/%Y",
        "%Y/%m/%d",
    ]
    for dt_format in valid_formats:
        try:
            datetime.strptime(dt_string, dt_format)
            return dt_format
        except ValueError:
            continue
    return False

def create_task(name: str,
                executor: str,
                filepath: str,
                trigger_type,
                event_id: str = None,
                start_date=None,
                start_time=None,
                end_date=None,
                end_time=None,
                location: str = '\\Scheduler',
                description: str = None):

    folder = scheduler.GetFolder(location)
    task_def = scheduler.NewTask(0)

    if start_date:
        date_format = _get_date_time_format(start_date)
        if date_format:
            dt_obj = datetime.strptime(start_date, date_format)
        else:
            return "Invalid start_date"
    else:
        dt_obj = datetime.now()

    if start_time:
        time_format = _get_date_time_format(start_time)
        if time_format:
            tm_obj = datetime.strptime(start_time, time_format)
        else:
            return "Invalid start_time"
    else:
        if trigger_type == 'Event':
            tm_obj=None
        else:
            print('Necessario informar o horario desejado')

    dt_end_obj = None
    if end_date:
        date_format = _get_date_time_format(end_date)
        if date_format:
            dt_end_obj = datetime.strptime(end_date, date_format)
        else:
            return "Invalid end_date"
    else:
        dt_end_obj = None

    if end_time:
        time_format = _get_date_time_format(end_time)
        if time_format:
            tm_end_obj = datetime.strptime(end_time, time_format)
        else:
            return "Invalid end_time"
    else:
        tm_end_obj = None

    if tm_obj:
        start_boundary = "{}T{}".format(
            dt_obj.strftime("%Y-%m-%d"), tm_obj.strftime("%H:%M:%S"))
    else:
        start_boundary = None

    end_boundary = None
    if dt_end_obj and tm_end_obj:
        end_boundary = "{}T{}".format(
            dt_end_obj.strftime("%Y-%m-%d"), tm_end_obj.strftime("%H:%M:%S")
        )

    # Trigger creation and settings
    trigger = task_def.Triggers.Create(trigger_types[trigger_type])
    if start_boundary:
        trigger.StartBoundary = start_boundary
    if end_boundary:
            trigger.EndBoundary = end_boundary

    if trigger_types[trigger_type] == TASK_TRIGGER_EVENT:
        if event_id:
            trigger.Subscription = f"""
            <QueryList>
            <Query Id="0" Path="Microsoft-Windows-TaskScheduler/Operational">
                <Select Path="Microsoft-Windows-TaskScheduler/Operational">*[EventData[@Name='TaskSuccessEvent'][Data[@Name='TaskName']='{location}\{event_id}']]</Select>
            </Query>
            </QueryList>
            """
        else:
            print('Necessario informar o id do evento mae')

    # Create action
    TASK_ACTION_EXEC = 0
    action = task_def.Actions.Create(TASK_ACTION_EXEC)
    action.ID = name
    action.Path = executor
    action.Arguments = filepath

    # Set parameters
    if description:
        task_def.RegistrationInfo.Description = description
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False

    # Register task
    # If task already exists, it will be updated
    TASK_CREATE_OR_UPDATE = 6
    TASK_LOGON_NONE = 0
    folder.RegisterTaskDefinition(
        name,  # Task name
        task_def,
        TASK_CREATE_OR_UPDATE,
        '',  # No user
        '',  # No password
        TASK_LOGON_NONE
    )

create_task("teste", 
            executor=r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE", 
            filepath=r"C:\Users\victo\Desktop\Python\windows_scheduler\teste.docx",
            trigger_type='Once',
            start_time='22:00',
            event_id='abre word')