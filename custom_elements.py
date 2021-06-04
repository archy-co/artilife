"""Custom visual elements for schemdraw library"""

from schemdraw.segments import Segment, SegmentText, SegmentCircle
import schemdraw.elements as sd_elem


class Constant(sd_elem.Element):
    """Element that holds one value all time"""

    def __init__(self, *d, constant_value: bool = True, lbl_size: float = 10,
                 **kwargs):
        super().__init__(*d, **kwargs)

        self.clen = 0.5
        self.cheight = 0.9

        self.segments.append(Segment([(-self.clen / 2, -self.cheight / 2),
                                      (-self.clen / 2, self.cheight / 2),
                                      (self.clen / 2, self.cheight / 2),
                                      (self.clen / 2, -self.cheight / 2),
                                      (-self.clen / 2, -self.cheight / 2)]))

        self.segments.append(Segment([(self.clen / 2, 0),
                                      (self.clen / 2 + 0.2, 0)]))
        self.segments.append(SegmentText((0, 0),
                                         str(int(constant_value)),
                                         fontsize=lbl_size))

        self.anchors['out'] = (self.clen / 2 + 0.2, 0)
        self.anchors['center'] = (0, 0)


class Variable(Constant):
    def __init__(self, *d, constant_value: bool = True, lbl_size: float = 10,
                 **kwargs):
        super().__init__(*d, constant_value=constant_value, lbl_size=lbl_size,
                         **kwargs)

        self.segments.append(
            SegmentCircle((-self.clen / 6, self.cheight / 3), 0.01, fill=None))
        self.segments.append(
            SegmentCircle((self.clen / 6, self.cheight / 3), 0.01, fill=None))
        self.segments.append(Segment([(-self.clen / 6, self.cheight / 3),
                                      (self.clen / 6,
                                       self.cheight / 3 + self.cheight / 12)]))
