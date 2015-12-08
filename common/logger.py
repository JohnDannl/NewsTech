#/usr/bin/env python
#_*_ coding:utf-8 _*_

def initlog(logfile='../newsCrawl.log'):
    import logging
    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return logger

log = initlog()
if __name__ == "__main__":
    log.debug("this is debug test")
    log.error('this is error test')
