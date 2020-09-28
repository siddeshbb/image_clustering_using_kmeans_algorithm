def compare(codebook, pixel):
    avg = 0
    returning = codebook[0]
    for index, code in enumerate(codebook):
        diff = sum(abs(x-y) for x in code for y in pixel)/3.0
        print diff, code
        if index == 0:
            avg = diff
            returning = code
        elif diff < avg:
            avg = diff
            returning = code
    return returning

print compare([(158, 10, 58), (214, 27, 112), (253, 246, 251)], (214, 255, 10))
