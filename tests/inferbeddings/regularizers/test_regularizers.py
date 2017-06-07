# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf

from inferbeddings.regularizers import TransEEquivalentPredicateRegularizer,\
    DistMultEquivalentPredicateRegularizer,\
    ComplExEquivalentPredicateRegularizer

import pytest


def l2sqr(x):
    return np.sum(np.square(x), axis=-1)


def complex_conjugate(x):
    x_re, x_im = np.split(x, indices_or_sections=2, axis=-1)
    return np.concatenate((x_re, - x_im), axis=-1)


@pytest.mark.light
def test_translations():
    rs = np.random.RandomState(0)
    pe = rs.rand(1024, 10)

    var = tf.Variable(pe, name='pe')

    init_op = tf.global_variables_initializer()
    with tf.Session() as session:
        session.run(init_op)

        loss = TransEEquivalentPredicateRegularizer(x1=var[0, :], x2=var[0, :])()
        np.testing.assert_almost_equal(session.run(loss), 0.0)

        loss = TransEEquivalentPredicateRegularizer(x1=var[0, :], x2=var[1, :])()
        np.testing.assert_almost_equal(session.run(loss), l2sqr(pe[0, :] - pe[1, :]))

        loss = TransEEquivalentPredicateRegularizer(x1=var[0:4, :], x2=var[0:4, :])()
        np.testing.assert_almost_equal(session.run(loss), [0.0] * 4)

        loss = TransEEquivalentPredicateRegularizer(x1=var[0, :], x2=var[1, :], is_inverse=True)()
        np.testing.assert_almost_equal(session.run(loss), l2sqr(pe[0, :] + pe[1, :]))

        loss = TransEEquivalentPredicateRegularizer(x1=var[0:4, :], x2=var[1:5, :])()
        np.testing.assert_almost_equal(session.run(loss), l2sqr(pe[0:4, :] - pe[1:5, :]))

        loss = TransEEquivalentPredicateRegularizer(x1=var[0:4, :], x2=var[1:5, :], is_inverse=True)()
        np.testing.assert_almost_equal(session.run(loss), l2sqr(pe[0:4, :] + pe[1:5, :]))

    tf.reset_default_graph()


@pytest.mark.light
def test_scaling():
    rs = np.random.RandomState(0)
    pe = rs.rand(1024, 10)

    var = tf.Variable(pe, name='pe')

    init_op = tf.global_variables_initializer()
    with tf.Session() as session:
        session.run(init_op)

        loss = DistMultEquivalentPredicateRegularizer(x1=var[0, :], x2=var[0, :])()
        np.testing.assert_almost_equal(session.run(loss), 0.0)

        loss = DistMultEquivalentPredicateRegularizer(x1=var[0, :], x2=var[1, :])()
        np.testing.assert_almost_equal(session.run(loss), l2sqr(pe[0, :] - pe[1, :]))

        loss = DistMultEquivalentPredicateRegularizer(x1=var[0:4, :], x2=var[0:4, :])()
        np.testing.assert_almost_equal(session.run(loss), [0.0] * 4)

        loss = DistMultEquivalentPredicateRegularizer(x1=var[0, :], x2=var[1, :], is_inverse=True)()
        np.testing.assert_almost_equal(session.run(loss), l2sqr(pe[0, :] - pe[1, :]))

        loss = DistMultEquivalentPredicateRegularizer(x1=var[0:4, :], x2=var[1:5, :])()
        np.testing.assert_almost_equal(session.run(loss), l2sqr(pe[0:4, :] - pe[1:5, :]))

        loss = DistMultEquivalentPredicateRegularizer(x1=var[0:4, :], x2=var[1:5, :], is_inverse=True)()
        np.testing.assert_almost_equal(session.run(loss), l2sqr(pe[0:4, :] - pe[1:5, :]))

    tf.reset_default_graph()


@pytest.mark.light
def test_complex():
    rs = np.random.RandomState(0)
    pe = rs.rand(1024, 10)

    var = tf.Variable(pe, name='pe')

    init_op = tf.global_variables_initializer()
    with tf.Session() as session:
        session.run(init_op)

        loss = ComplExEquivalentPredicateRegularizer(x1=var[0, :], x2=var[0, :])()
        np.testing.assert_almost_equal(session.run(loss), 0.0)

        loss = ComplExEquivalentPredicateRegularizer(x1=var[0, :], x2=var[1, :])()
        np.testing.assert_almost_equal(session.run(loss), l2sqr(pe[0, :] - pe[1, :]))

        loss = ComplExEquivalentPredicateRegularizer(x1=var[0:4, :], x2=var[0:4, :])()
        np.testing.assert_almost_equal(session.run(loss), [0.0] * 4)

        loss = ComplExEquivalentPredicateRegularizer(x1=var[0, :], x2=var[1, :], is_inverse=True)()
        np.testing.assert_almost_equal(session.run(loss), l2sqr(pe[0, :] - complex_conjugate(pe[1, :])))

        loss = ComplExEquivalentPredicateRegularizer(x1=var[0:4, :], x2=var[1:5, :])()
        np.testing.assert_almost_equal(session.run(loss), l2sqr(pe[0:4, :] - pe[1:5, :]))

        loss = ComplExEquivalentPredicateRegularizer(x1=var[0:4, :], x2=var[1:5, :], is_inverse=True)()
        np.testing.assert_almost_equal(session.run(loss), l2sqr(pe[0:4, :] - complex_conjugate(pe[1:5, :])))

    tf.reset_default_graph()

if __name__ == '__main__':
    pytest.main([__file__])
