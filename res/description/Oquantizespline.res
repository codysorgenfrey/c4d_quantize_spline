CONTAINER Oquantizespline {
    INCLUDE Obase;
    NAME Oquantizespline;
    GROUP ID_OBJECTPROPERTIES {
    }
    GROUP QUANTIZE_SPLINE_GROUP {
        DEFAULT 1;
        LONG QUANTIZE_SPLINE_ORDER {
            DEFAULT QUANTIZE_SPLINE_ORDER_XYZ;
            CYCLE {
                QUANTIZE_SPLINE_ORDER_XYZ;
                QUANTIZE_SPLINE_ORDER_XZY;
                QUANTIZE_SPLINE_ORDER_YXZ;
                QUANTIZE_SPLINE_ORDER_YZX;
                QUANTIZE_SPLINE_ORDER_ZYX;
                QUANTIZE_SPLINE_ORDER_ZXY;
            }
        }
    }
}
