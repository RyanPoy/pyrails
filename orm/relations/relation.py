#coding: utf8
from collections import OrderedDict as oDict
from queue import Queue as Q
from sweet.utils.inflection import *


class RelationQ(Q):
    def get(self, block=True, timeout=None):
        if self.qsize() > 0:
            return super().get(block=block, timeout=timeout)
        return None
relation_q = RelationQ()


class Relation(object):

    pass

