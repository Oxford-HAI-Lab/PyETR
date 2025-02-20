from pysmt.environment import Environment

from pyetr import View
from pyetr.parsing.smt_lib_parser.view_to_smt_lib import views_to_smt_lib
from pyetr.utils import smt_lib_to_views

string = """
(declare-sort U 0)
(declare-fun Student (U) Bool)
(declare-fun Professor (U) Bool)
(declare-fun Book (U) Bool)
(declare-fun Teaches (U U) Bool)
(declare-fun Reads (U U) Bool)

(assert
 (forall
  ((x U))
  (exists
   ((y U))
   (=> (Professor x)
       (and
        (Teaches x y)
        (Student y)
        (Professor x))))))

(assert
 (forall
  ((z U))
  (exists
   ((w U))
   (=> (Student z)
       (and
        (Book w)
        (Reads z w)
        (Student z))))))

(assert
  (exists
   ((y U) (b U))
   (or true
       (and (Book b)
            (Reads y b)))))
"""
out = smt_lib_to_views(string)
print(out)
new = views_to_smt_lib(out)
print(new)
