from pyspark.sql import DataFrame

from optimus.helpers.decorators import *

from pyspark.sql.functions import array, col, explode, lit, struct
from pyspark.sql import DataFrame


@add_method(DataFrame)
#def melt(self, id_vars, value_vars, var_name, value_name):
def melt(self, id_vars, value_vars, var_name="variable", value_name="value"):
    """
    Convert :class:'DataFrame' from wide to long format.
    """
    _vars_and_vals = array(*(struct(lit(c).alias(var_name), col(c).alias(value_name)) for c in value_vars))

    # Add to the DataFrame and explode
    tmp = self.withColumn("_vars_and_vals", explode(_vars_and_vals))

    cols = id_vars + [col("_vars_and_vals")[x].alias(x) for x in [var_name, value_name]]

    return tmp.select(*cols)
