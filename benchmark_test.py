start = get_time()
op_start = get_op_count()


farm_cacti(112000)


cnt = get_op_count() - op_start
dur = get_time() - start

print("took", dur, "s and", cnt, "ops")
