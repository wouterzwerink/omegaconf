# -*- coding: utf-8 -*-
import os
import tempfile
import io
from omegaconf import OmegaConf
import six


def save_load_file(conf):
    with tempfile.NamedTemporaryFile(mode="wt") as fp:
        conf.save(fp.file)
        fp.seek(0)
        with io.open(os.path.abspath(fp.name), 'rt') as handle:
            c2 = OmegaConf.load(handle)
        assert conf == c2


def save_load_filename(conf):
    # note that delete=False here is a work around windows incompetence.
    try:
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            conf.save(fp.name)
            c2 = OmegaConf.load(fp.name)
            assert conf == c2
    finally:
        os.unlink(fp.name)


def test_save_load_file():
    save_load_file(OmegaConf.create(dict(a=10)))


def test_save_load_filename():
    save_load_filename(OmegaConf.create(dict(a=10)))


def test_pickle_dict():
    with tempfile.TemporaryFile() as fp:
        import pickle
        c = OmegaConf.create(dict(a='b'))
        pickle.dump(c, fp)
        fp.flush()
        fp.seek(0)
        c1 = pickle.load(fp)
        assert c == c1


def test_pickle_list():
    with tempfile.TemporaryFile() as fp:
        import pickle
        c = OmegaConf.create([1, 2, 3])
        pickle.dump(c, fp)
        fp.flush()
        fp.seek(0)
        c1 = pickle.load(fp)
        assert c == c1


def test_save_load_unicode():
    save_load_filename(OmegaConf.create([(u"היי,", u"מה נשמע?")]))