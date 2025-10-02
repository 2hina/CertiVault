# ==============================================================================
# Binary Search Algorithm
# This function efficiently searches for a target value within a sorted list (array).
# Time Complexity: O(log n) - highly efficient for large datasets.
# Prerequisite: The input array MUST be sorted.
# ==============================================================================
def binary_search(arr, target):
    """
    Searches for the target value in a sorted array using the binary search method.

    :param arr: The sorted list of numbers to search within.
    :param target: The value to search for.
    :return: The index of the target if found, otherwise -1.
    """
    # Initialize the pointers for the search range
    low = 0
    high = len(arr) - 1

    # Loop continues as long as the search range is valid (low <= high)
    while low <= high:
        # Calculate the middle index using integer division
        # This is the 'guess' where the target might be
        mid = (low + high) // 2
        
        # Case 1: Target found!
        if arr[mid] == target:
            return mid
        
        # Case 2: Target is in the upper half.
        # Discard the left half of the array by moving the low pointer.
        elif arr[mid] < target:
            low = mid + 1
            
        # Case 3: Target is in the lower half.
        # Discard the right half of the array by moving the high pointer.
        else:
            high = mid - 1
            
    # If the loop finishes without finding the target, return -1
    return -1

# --- Example Usage ---
if __name__ == "__main__":
    # The array MUST be sorted for binary search to work
    sorted_numbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    
    target_value_found = 23
    target_value_missing = 42

    # Search for a value that exists
    index_found = binary_search(sorted_numbers, target_value_found)
    print(f"Searching for {target_value_found} in the list...")
    if index_found != -1:
        print(f"Element found at index: {index_found}")
    else:
        print("Element not found.")

    # Search for a value that does not exist
    index_missing = binary_search(sorted_numbers, target_value_missing)
    print(f"\nSearching for {target_value_missing} in the list...")
    if index_missing != -1:
        print(f"Element found at index: {index_missing}")
    else:
        print("Element not found.")
