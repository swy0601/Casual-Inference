                    displacement.z+=nodeCoefficient.z * basis;
                    basis = xFirst.z * tempBasis.x;
                    Tx_x+=nodeCoefficient.x * basis;
                    Ty_x+=nodeCoefficient.y * basis;
                    Tz_x+=nodeCoefficient.z * basis;
                    basis = xBasis.z * tempBasis.y;
                    Tx_y+=nodeCoefficient.x * basis;
                    Ty_y+=nodeCoefficient.y * basis;
                    Tz_y+=nodeCoefficient.z * basis;
                    basis = xBasis.z * tempBasis.z;
                    Tx_z+=nodeCoefficient.x * basis;
                    Ty_z+=nodeCoefficient.y * basis;
                    Tz_z+=nodeCoefficient.z * basis;
                    nodeCoefficient = tex1Dfetch(controlPointTexture,indexXYZ);
                    basis = xBasis.w * tempBasis.x;
                    displacement.x+=nodeCoefficient.x * basis;
                    displacement.y+=nodeCoefficient.y * basis;
                    displacement.z+=nodeCoefficient.z * basis;
                    basis = xFirst.w * tempBasis.x;
                    Tx_x+=nodeCoefficient.x * basis;
                    Ty_x+=nodeCoefficient.y * basis;
                    Tz_x+=nodeCoefficient.z * basis;
                    basis = xBasis.w * tempBasis.y;
                    Tx_y+=nodeCoefficient.x * basis;
                    Ty_y+=nodeCoefficient.y * basis;
                    Tz_y+=nodeCoefficient.z * basis;
                    basis = xBasis.w * tempBasis.z;
                    Tx_z+=nodeCoefficient.x * basis;
                    Ty_z+=nodeCoefficient.y * basis;
                    Tz_z+=nodeCoefficient.z * basis;
