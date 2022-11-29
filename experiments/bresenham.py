def bresenham3D(curr_a, curr_b, curr_c, dest_a, dest_b, dest_c):
    pos_a = curr_a
    pos_b = curr_b
    pos_c = curr_c
    da = abs(dest_a - curr_a)
    db = abs(dest_b - curr_b)
    dc = abs(dest_c - curr_c)
    
    dir_a = 1 if dest_a > curr_a else -1
    dir_b = 1 if dest_b > curr_b else -1
    dir_c = 1 if dest_c > curr_c else -1
    
    if da >= db and da >= dc:
        temp_b = 0
        temp_c = 0
        step_b = db / da
        step_c = dc / da

        for x in range(da):
            pos_a = pos_a + 1
            temp_b = temp_b + step_b
            temp_c = temp_c + step_c
            
            if temp_b >= 1:
                temp_b = temp_b - 1
                pos_b = pos_b + 1

            if temp_c >= 1:
                temp_c = temp_c - 1
                pos_c = pos_c + 1
            print(pos_a, pos_b, pos_c)
    elif db >= da and db >= dc:
        temp_a = 0
        temp_c = 0
        step_a = da / db
        step_c = dc / db

        for x in range(db):
            pos_b = pos_b + 1
            temp_a = temp_a + step_a
            temp_c = temp_c + step_c
            
            if temp_a >= 1:
                temp_a = temp_a - 1
                pos_a = pos_a + 1

            if temp_c >= 1:
                temp_c = temp_c - 1
                pos_c = pos_c + 1
            print(pos_a, pos_b, pos_c)

    elif dc >= da and dc >= db:
        temp_a = 0
        temp_b = 0
        step_a = da / dc
        step_b = db / dc

        for x in range(dc):
            pos_c = pos_c + 1
            temp_a = temp_a + step_a
            temp_b = temp_b + step_b
            
            if temp_a >= 1:
                temp_a = temp_a - 1
                pos_a = pos_a + 1

            if temp_b >= 1:
                temp_b = temp_b - 1
                pos_b = pos_b + 1
            print(pos_a, pos_b, pos_c)



bresenham3D(0,0,0, 10, 20, 50)