from builtins import zip
from ..frame import H2OFrame
import h2o
from h2o.utils.compatibility import assert_is_type
from .model_base import ModelBase

class H2OMultinomialModel(ModelBase):

  def _make_model(self):
    return H2OMultinomialModel()

  def confusion_matrix(self, data):
    """
    Returns a confusion matrix based of H2O's default prediction threshold for a dataset
    """
    assert_is_type(data, "data", H2OFrame)
    j = h2o.api("POST /3/Predictions/models/%s/frames/%s" % (self._id, data.frame_id))
    return j["model_metrics"][0]["cm"]["table"]

  def hit_ratio_table(self, train=False, valid=False, xval=False):
    """
    Retrieve the Hit Ratios

    If all are False (default), then return the training metric value.
    If more than one options is set to True, then return a dictionary of metrics where the keys are "train", "valid",
    and "xval"

    :param train: If train is True, then return the R^2 value for the training data.
    :param valid: If valid is True, then return the R^2 value for the validation data.
    :param xval:  If xval is True, then return the R^2 value for the cross validation data.
    :return: The R^2 for this regression model.
    """
    tm = ModelBase._get_metrics(self, train, valid, xval)
    m = {}
    for k,v in zip(list(tm.keys()),list(tm.values())): m[k] = None if v is None else v.hit_ratio_table()
    return list(m.values())[0] if len(m) == 1 else m


  def mean_per_class_error(self, train=False, valid=False, xval=False):
    """
    Retrieve the mean per class error across all classes

    If all are False (default), then return the training metric value.
    If more than one options is set to True, then return a dictionary of metrics where the keys are "train", "valid",
    and "xval"

    Parameters
    ----------
      train : bool, optional
        If True, return the mean_per_class_error value for the training data.

      valid : bool, optional
        If True, return the mean_per_class_error value for the validation data.

      xval : bool, optional
        If True, return the mean_per_class_error value for each of the cross-validated splits.

    Returns
    -------
      The mean_per_class_error values for the specified key(s).
    """
    tm = ModelBase._get_metrics(self, train, valid, xval)
    m = {}
    for k,v in zip(list(tm.keys()),list(tm.values())): m[k] = None if v is None else v.mean_per_class_error()
    return list(m.values())[0] if len(m) == 1 else m

  def plot(self, timestep="AUTO", metric="AUTO", **kwargs):
    """
    Plots training set (and validation set if available) scoring history for an H2OMultinomialModel. The timestep and metric
    arguments are restricted to what is available in its scoring history.

    :param timestep: A unit of measurement for the x-axis.
    :param metric: A unit of measurement for the y-axis.
    :return: A scoring history plot.
    """

    if self._model_json["algo"] in ("deeplearning", "drf", "gbm"):
      if metric == "AUTO": metric = "classification_error"
      elif metric not in ("logloss","classification_error","rmse"):
        raise ValueError("metric for H2OMultinomialModel must be one of: AUTO, logloss, classification_error, rmse")

    self._plot(timestep=timestep, metric=metric, **kwargs)
