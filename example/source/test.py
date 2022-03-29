for item in container:
    if search_something(item):
        # Found it!
        process(item)
        break
    else:
    # Didn't find anything..
    not_found_in_container()
   
