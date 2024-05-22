def read_input():
    """
    Reads the user input to be used in website search 
    """
    name = input("Enter a restaraunt name: ")
    city = input("Enter the name of a city: ")
    return name, city


def get_user_selection(search_results: list):
    """
    :param search_results - a list of search results in the form of (name, address)
    
    return - the index of the selected search result
    """
    for i in range(len(search_results)):
        print(str(i) + ": " + str(search_results[i]))
    selection = input("Enter a number to select what restaraunt you had in mind: ")
    return int(selection)