from django.db import connection


def importer(data, TABLE_NAME):
    #create query
    #col = data[0]
    a_col = list(data[0].keys())
    if (a_col[0] == "\ufeffId"):
        a_col[0] = 'Id'
    cols = ', '.join(a_col)
    step = 5000
    rows_inserted = 0
    tmp_counter = 0
    q = f'INSERT INTO {TABLE_NAME} ({cols}) VALUES '
    try:
        for j, items in enumerate(data, 1):
            flag = False
            items['EntityCreatedAt'] = items['EntityCreatedAt'][:26]
            items['EntityModifiedAt'] = items['EntityModifiedAt'][:26]
            s = str(tuple(items.values()))
            s = s + ', ' if (j%step !=0) else s
            q += s
            tmp_counter += 1
            if (j%step==0):
                tmp_counter = 0
                flag = True
                with connection.cursor() as cursor:
                    cursor.execute(q)
                    rows_inserted += step
                q = f'INSERT INTO {TABLE_NAME} ({cols}) VALUES '

        #s = str(tuple(items.values()))
        #q += s
        if(not flag):
            q = q[:-2]
            with connection.cursor() as cursor:
                cursor.execute(q)
                rows_inserted += tmp_counter
    except:
        return rows_inserted
    return rows_inserted
