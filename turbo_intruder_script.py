def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=100,

                           # 并发时可修改engine类型为THREADED
                           # engine=Engine.THREADED,

                           # HTTP2时修改engine类型为HTTP2
                           # engine=Engine.HTTP2,
                           )
    """
        以下为示例代码，可根据实际情况修改。注意不能同时运行，只能选择一种爆破方式。其它的可以注释掉。
    """

    ### 单参数爆破代码开始 ###
    # login?username=admin&password=%s
    # 从usr/share/dict/words中读取字典

    #for word in open('/usr/share/dict/words'):
    #    # 将字典中的每个单词加入到请求队列中
    #    engine.queue(target.req, word.rstrip())

    ### 单参数爆破代码结束 ###


    ### 多参数爆破代码开始 ###
    # login?username=%s&password=%s
    # 多参数爆破，遍历账号密码两个字典

    # for user in open('/usr/share/dict/words'):
    #     for passwd in open('/usr/share/dict/words'):
    #         # 使用[]的方式传递多个参数
    #         engine.queue(target.req, [user.rstrip(), passwd.rstrip()])

    ### 多参数爆破代码结束 ###


    ### 并发请求代码开始 ###
    # 增加请求头：req: %s
    # 100个请求并发
    # 注意，这里的并发数量，要小于上面engine配置的 concurrentConnections * requestsPerConnection 的数量

    for i in range(100):
        engine.queue(target.req, i, gate='race')
    engine.openGate('race')
    time.sleep(1)

    ### 并发请求代码结束 ###


def handleResponse(req, interesting):
    # 退出条件，根据实际情况修改
    max_cost = 1000  # 最大请求时间，超出即退出，单位毫秒
    ex_status = [503, 502]  # 遇到503， 502即退出

    # 保存结果，根据实际情况修改
    save_result = False # 是否保存结果，True保存，False不保存
    save_path = '/Users/demo/result.txt'  # 保存结果的路径，目录不存在会执行异常

    cancel_condition = req.time > max_cost * 1000 or req.status in ex_status

    if cancel_condition:
        req.engine.cancel()

    # 如果save_result为True，则将结果保存到save_path中
    if save_result:
        with open(save_path, "a") as file:
            file.write(req.response)
            file.flush()

    if req.status != 404:
        table.add(req)
