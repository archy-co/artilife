"""Custom visual elements for schemdraw library"""

from schemdraw.segments import Segment, SegmentText
import schemdraw.elements as sd_elem


class Constant(sd_elem.Element):
    """Element that holds one value all time"""

    def __init__(self, *d, constant_value: bool = True, lbl_size: float = 10, **kwargs):
        super().__init__(*d, **kwargs)

        clen = 0.5
        cheight = 0.9

        self.segments.append(Segment([(-clen / 2, -cheight / 2),
                                      (-clen / 2, cheight / 2),
                                      (clen / 2, cheight / 2),
                                      (clen / 2, -cheight / 2),
                                      (-clen / 2, -cheight / 2)]))
        self.segments.append(Segment([(clen / 2, 0),
                                      (clen / 2 + 0.2, 0)]))
        self.segments.append(SegmentText((0, 0),
                                         str(int(constant_value)),
                                         fontsize=lbl_size))

        self.anchors['out'] = (clen / 2 + 0.2, 0)
        self.anchors['center'] = (0, 0)


class Variable(Constant):
    def __init__(self, *d, constant_value: bool = True, lbl_size: float = 10, **kwargs):
        super().__init__(*d, constant_value=constant_value, lbl_size=lbl_size, **kwargs)
