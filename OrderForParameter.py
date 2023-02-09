def OrderForParameter():
    v = Vlevel()
    w = today.weekday()
    # 0 ~ 4 월 ~ 금

    if w == 0:
        if v < 4:
            OneStopOrder(2, 'c', 's')
            OneStopOrder(2, 'p', 's')
        if v > 5:
            OneStopOrder(3, 'c', 's')
            OneStopOrder(3, 'p', 's')
        if v == 4:
            OneStopOrder(3, 'c', 's')
            OneStopOrder(3, 'p', 's')
            OneStopOrder(1, 'c', 'b')
            OneStopOrder(1, 'p', 'b')
        if v == 5:
            OneStopOrder(3, 'c', 's')
            OneStopOrder(3, 'p', 's')

    if w == 1:
        if v < 4:
            OneStopOrder(2, 'c', 's')
            OneStopOrder(2, 'p', 's')
            OneStopOrder(1, 'c', 'b')
            OneStopOrder(1, 'p', 'b')
        if v == 4:
            OneStopOrder(2, 'c', 's')
            OneStopOrder(3, 'p', 's')
        if v > 5:
            OneStopOrder(1, 'c', 's')
            OneStopOrder(1, 'p', 's')
            OneStopOrder(2, 'c', 'b')
            OneStopOrder(2, 'p', 'b')

    if w == 2:
        if v < 4:
            OneStopOrder(2, 'c', 's')
            OneStopOrder(2, 'p', 's')
            OneStopOrder(1, 'c', 'b')
            OneStopOrder(1, 'p', 'b')
        if v > 5:
            OneStopOrder(2, 'c', 's')
            OneStopOrder(3, 'p', 's')
        if v == 4:
            OneStopOrder(3, 'c', 's')
            OneStopOrder(3, 'p', 's')
            OneStopOrder(2, 'c', 'b')
            OneStopOrder(2, 'p', 'b')
        if v == 5:
            OneStopOrder(4, 'c', 's')
            OneStopOrder(4, 'p', 's')
            OneStopOrder(3, 'c', 'b')
            OneStopOrder(3, 'p', 'b')

    if w == 3:
        if v < 4:
            OneStopOrder(2, 'c', 's')
            OneStopOrder(3, 'p', 's')
        if v > 5:
            OneStopOrder(3, 'c', 's')
            OneStopOrder(3, 'p', 's')
        if v == 5:
            OneStopOrder(1, 'c', 's')
            OneStopOrder(1, 'p', 's')

    if w == 4:
        if v == 4:
            OneStopOrder(1, 'c', 's')
            OneStopOrder(2, 'p', 's')
        if v > 5:
            OneStopOrder(1, 'c', 's')
            OneStopOrder(1, 'p', 's')
        if v == 5:
            OneStopOrder(4, 'c', 's')
            OneStopOrder(4, 'p', 's')

    return;