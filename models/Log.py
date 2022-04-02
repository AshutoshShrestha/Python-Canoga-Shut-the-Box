class Log:
    # Function Name: __init__
    # Purpose: To initialize the Log class 
    # Parameters:
    #             
    # Return Value: none (void)
    # Algorithm:
    #             1) Initialize a new list to store all logs
    # Assistance Received: none 
    def __init__(self):
        self.log_message = list()

    # Function Name: add_log
    # Purpose: To append latest log to total log
    # Parameters:
    #             message, a string that holds the latest log
    # Return Value: none (void)
    # Algorithm:
    #             1) Append the message to the log_message list
    # Assistance Received: none 
    def add_log(self, message):
        print(message)
        self.log_message.append(message)

    # Function Name: get_all_log
    # Purpose: To return the whole log 
    # Parameters:
    #             
    # Return Value: log_message, a list of log messages
    # Algorithm:
    #             1) Return log_message list
    # Assistance Received: none 
    def get_all_log(self):
        return self.log_message

    # Function Name: get_last_log
    # Purpose: To get the latest log 
    # Parameters:
    #             
    # Return Value: latest_log, the most recent entry in the log_message list
    # Algorithm:
    #             1) Return the most recent entry from the logs list.
    # Assistance Received: none 
    def get_last_log(self):
        return self.log_message[len(self.log_message)-1]

        
