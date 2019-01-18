__global__ void updateV(SDL_Rect *cells, float *u1, float *u2, float *u3, float *v, int t, int *s, float *c, int nX, int nY, float dTime){
    int num = blockIdx.x * blockDim.x + threadIdx.x;
    int cT = 1;
    float rightU1, bottomU1, leftU1, topU1;
    float rightU2, bottomU2, leftU2, topU2;
    float rightU3, bottomU3, leftU3, topU3;
    float uT = u1[num], vT = v[num], dTemp, dV;
    float rightV, bottomV, leftV, topV;
    int width = cells[num].w, height = cells[num].h;
    if(s[num] != 0){
        if(s[num] == t){
            v[num] = 1000;
            return;
        }
        if((s[num] == 1) || (s[num] == 2) || (s[num] == 3)){
            v[num] = 0;
        }
    }
    if(num < nX){
        if(num == 0){
            rightU1  = u1[num + 1];
            bottomU1 = u1[num + nX];
            rightU2  = u2[num + 1];
            bottomU2 = u2[num + nX];
            rightU3  = u3[num + 1];
            bottomU3 = u3[num + nX];
            rightV  = v[num + 1];
            bottomV = v[num + nX];
            dV = cT * ((rightV - vT) / pow(width, 2)) +
                 cT * ((-vT + bottomV) / pow(height, 2));
            if(dV == 0){
                return;
            }
            dTemp = dV -
                    c[0] * ((rightU1 - uT) / pow(width, 2)) -
                    c[0] * ((-uT + bottomU1) / pow(height, 2)) -
                    c[0] * ((rightU2 - uT) / pow(width, 2)) -
                    c[0] * ((-uT + bottomU2) / pow(height, 2)) -
                    c[0] * ((rightU3 - uT) / pow(width, 2)) -
                    c[0] * ((-uT + bottomU3) / pow(height, 2));
            float newV = v[num] + dTemp * dTime;
            if(newV < 0){
                v[num] = 0.0f;
                return;
            }
            v[num] = newV;
            return;
        }
        if((num + 1) == nX){
            leftU1   = u1[num - 1];
            bottomU1 = u1[num + nX];
            leftU2   = u2[num - 1];
            bottomU2 = u2[num + nX];
            leftU3   = u3[num - 1];
            bottomU3 = u3[num + nX];
            leftV   = v[num - 1];
            bottomV = v[num + nX];
            dV = cT * ((-vT + leftV) / pow(width, 2)) + 
                 cT * ((-vT + bottomV) / pow(height, 2));
            if(dV == 0){
                return;
            }
            dTemp = dV -
                    c[0] * ((-uT + leftU1) / pow(width, 2)) - 
                    c[0] * ((-uT + bottomU1) / pow(height, 2)) -
                    c[1] * ((-uT + leftU2) / pow(width, 2)) - 
                    c[1] * ((-uT + bottomU2) / pow(height, 2)) -
                    c[2] * ((-uT + leftU3) / pow(width, 2)) - 
                    c[2] * ((-uT + bottomU3) / pow(height, 2));
            float newV = v[num] + dTemp * dTime;
            if(newV < 0){
                v[num] = 0.0f;
                return;
            }
            v[num] = newV;
            return;
        }
        rightU1  = u1[num + 1];
        leftU1   = u1[num - 1];
        bottomU1 = u1[num + nX];
        rightU2  = u2[num + 1];
        leftU2   = u2[num - 1];
        bottomU2 = u2[num + nX];
        rightU3  = u3[num + 1];
        leftU3   = u3[num - 1];
        bottomU3 = u3[num + nX];
        rightV  = v[num + 1];
        leftV   = v[num - 1];
        bottomV = v[num + nX];
        dV = cT * ((rightV - 2 * vT + leftV) / pow(width, 2)) +
             cT * ((-vT + bottomV) / pow(height, 2));
        if(dV == 0){
            return;
        }
        dTemp = dV -
                c[0] * ((rightU1 - 2 * uT + leftU1) / pow(width, 2)) -
                c[0] * ((-uT + bottomU1) / pow(height, 2)) -
                c[1] * ((rightU2 - 2 * uT + leftU2) / pow(width, 2)) -
                c[1] * ((-uT + bottomU2) / pow(height, 2)) -
                c[2] * ((rightU3 - 2 * uT + leftU3) / pow(width, 2)) -
                c[2] * ((-uT + bottomU3) / pow(height, 2)) ;
        float newV = v[num] + dTemp * dTime;
        if(newV < 0){
            v[num] = 0.0f;
            return;
        }
        v[num] = newV;
        return;
    }
    if((num + 1) > (nY * nX - nX)){
        if((num + 1) == (nY * nX - nX + 1)){
            rightU1  = u1[num + 1];
            topU1    = u1[num - nX];
            rightU2  = u2[num + 1];
            topU2    = u2[num - nX];
            rightU3  = u3[num + 1];
            topU3    = u3[num - nX];
            rightV  = v[num + 1];
            topV    = v[num - nX];
            dV = dTemp = cT * ((rightV - vT) / pow(width, 2)) + 
                    cT * ((topV - vT) / pow(height, 2));
            if(dV == 0){
                return;
            }
            dTemp = dV -
                    c[0] * ((rightU1 - uT) / pow(width, 2)) - 
                    c[0] * ((topU1 - uT) / pow(height, 2)) - 
                    c[1] * ((rightU2 - uT) / pow(width, 2)) - 
                    c[1] * ((topU2 - uT) / pow(height, 2)) -
                    c[2] * ((rightU3 - uT) / pow(width, 2)) - 
                    c[2] * ((topU3 - uT) / pow(height, 2));
            float newV = v[num] + dTemp * dTime;
            if(newV < 0){    
                v[num] = 0.0f;
                return;
            }
            v[num] = newV;
            return;
        }
        if((num + 1) == (nX * nY)){
            topU1    = u1[num - nX];
            leftU1   = u1[num - 1];
            topU2    = u2[num - nX];
            leftU2   = u2[num - 1];
            topU3    = u3[num - nX];
            leftU3   = u3[num - 1];
            leftV   = v[num - 1];
            topV    = v[num - nX];
            dV = cT * ((-vT + leftV) / pow(width, 2)) + 
                 cT * ((topV - vT) / pow(height, 2));
            if(dV == 0){
                return;
            }
            dTemp = dV -
                    c[0] * ((-uT + leftU1) / pow(width, 2)) - 
                    c[0] * ((topU1 - uT) / pow(height, 2)) -
                    c[1] * ((-uT + leftU2) / pow(width, 2)) - 
                    c[1] * ((topU2 - uT) / pow(height, 2)) -
                    c[2] * ((-uT + leftU3) / pow(width, 2)) - 
                    c[2] * ((topU3 - uT) / pow(height, 2));
            float newV = v[num] + dTemp * dTime;
            if(newV < 0){    
                v[num] = 0.0f;
                return;
            }
            v[num] = newV;
            return;
        }
        topU1    = u1[num - nX];
        leftU1   = u1[num - 1];
        rightU1  = u1[num + 1];
        topU2    = u2[num - nX];
        leftU2   = u2[num - 1];
        rightU2  = u2[num + 1];
        topU3    = u3[num - nX];
        leftU3   = u3[num - 1];
        rightU3  = u3[num + 1];
        rightV  = v[num + 1];
        leftV   = v[num - 1];
        topV    = v[num - nX];
        dV = cT * ((rightV - 2 * vT + leftV) / pow(width, 2)) + 
             cT * ((topV - vT) / pow(height, 2));
        if(dV == 0){
            return;
        }
        dTemp = dV -
                c[0] * ((rightU1 - 2 * uT + leftU1) / pow(width, 2)) - 
                c[0] * ((topU1 - uT) / pow(height, 2)) - 
                c[1] * ((rightU2 - 2 * uT + leftU2) / pow(width, 2)) - 
                c[1] * ((topU2 - uT) / pow(height, 2)) -
                c[2] * ((rightU3 - 2 * uT + leftU3) / pow(width, 2)) - 
                c[2] * ((topU3 - uT) / pow(height, 2));
        float newV = v[num] + dTemp * dTime;
        if(newV < 0){
            v[num] = 0.0f;
            return;
        }
        v[num] = newV;
        return;
    }
    if(((num + 1) % nX) == 1){
        topU1    = u1[num - nX];
        rightU1  = u1[num + 1];
        bottomU1 = u1[num + nX];
        topU2    = u2[num - nX];
        rightU2  = u2[num + 1];
        bottomU2 = u2[num + nX];
        topU3    = u3[num - nX];
        rightU3  = u3[num + 1];
        bottomU3 = u3[num + nX];
        rightV  = v[num + 1];
        topV    = v[num - nX];
        bottomV = v[num + nX];
        dV = cT * ((rightV - vT) / pow(width, 2)) + 
             cT * ((topV - 2 * vT + bottomV) / pow(height, 2));
        if(dV == 0){
            return;
        }
        dTemp = dV -
                c[0] * ((rightU1 - uT) / pow(width, 2)) -
                c[0] * ((topU1 - 2 * uT + bottomU1) / pow(height, 2)) -
                c[1] * ((rightU2 - uT) / pow(width, 2)) -
                c[1] * ((topU2 - 2 * uT + bottomU2) / pow(height, 2)) -
                c[2] * ((rightU3 - uT) / pow(width, 2)) -
                c[2] * ((topU3 - 2 * uT + bottomU3) / pow(height, 2));
        float newV = v[num] + dTemp * dTime;
        if(newV < 0){
            v[num] = 0.0f;
            return;
        }
        v[num] = newV;
        return;
    }
    if(((num + 1) % nX) == 0){
        leftU1   = u1[num - 1];
        topU1    = u1[num - nX];
        bottomU1 = u1[num + nX];
        leftU2   = u2[num - 1];
        topU2    = u2[num - nX];
        bottomU2 = u2[num + nX];
        leftU3   = u3[num - 1];
        topU3    = u3[num - nX];
        bottomU3 = u3[num + nX];
        leftV   = v[num - 1];
        topV    = v[num - nX];
        bottomV = v[num + nX];
        dV = cT * ((-vT + leftV) / pow(width, 2)) +
             cT * ((topV - 2 * vT + bottomV) / pow(height, 2));
        if(dV == 0){
            return;
        }
        dTemp = dV -
                c[0] * ((-uT + leftU1) / pow(width, 2)) -
                c[0] * ((topU1 - 2 * uT + bottomU1) / pow(height, 2)) -
                c[1] * ((-uT + leftU2) / pow(width, 2)) -
                c[1] * ((topU2 - 2 * uT + bottomU2) / pow(height, 2)) -
                c[2] * ((-uT + leftU3) / pow(width, 2)) -
                c[2] * ((topU3 - 2 * uT + bottomU3) / pow(height, 2));
        float newV = v[num] + dTemp * dTime;
        if(newV < 0){
            v[num] = 0.0f;
            return;
        }
        v[num] = newV;
        return;
    }
    rightU1  = u1[num + 1];
    leftU1   = u1[num - 1];
    topU1    = u1[num - nX];
    bottomU1 = u1[num + nX];
    rightU2  = u2[num + 1];
    leftU2   = u2[num - 1];
    topU2    = u2[num - nX];
    bottomU2 = u2[num + nX];
    rightU3  = u3[num + 1];
    leftU3   = u3[num - 1];
    topU3    = u3[num - nX];
    bottomU3 = u3[num + nX];
    rightV  = v[num + 1];
    leftV   = v[num - 1];
    topV    = v[num - nX];
    bottomV = v[num + nX];
    dV = cT * ((rightV - 2 * vT + leftV) / pow(width, 2)) + 
         cT * ((topV - 2 * vT + bottomV) / pow(height, 2));
    if(dV == 0){
        return;
    }
    dTemp = dV -
            c[0] * ((rightU1 - 2 * uT + leftU1) / pow(width, 2)) - 
            c[0] * ((topU1 - 2 * uT + bottomU1) / pow(height, 2)) -
            c[1] * ((rightU2 - 2 * uT + leftU2) / pow(width, 2)) - 
            c[1] * ((topU2 - 2 * uT + bottomU2) / pow(height, 2)) -
            c[2] * ((rightU3 - 2 * uT + leftU3) / pow(width, 2)) - 
            c[2] * ((topU3 - 2 * uT + bottomU3) / pow(height, 2));
    float newV = v[num] + dTemp * dTime;
    if(newV < 0){
        v[num] = 0.0f;
        return;
    }
    v[num] = newV;
    return;
}

__global__ void updateU(SDL_Rect * cells, float *u, int t, int *s, float c, int nX, int nY, float dTime){
    int num = blockIdx.x * blockDim.x + threadIdx.x;
    float right, bottom, left, top, temp = u[num], dTemp;
    int width = cells[num].w, height = cells[num].h;
    if(s[num] != 0){
        if(s[num] == t){
            u[num] = 1000;
            return;
        }
    }
    if(num < nX){
        if(num == 0){
            right  = u[num + 1];
            bottom = u[num + nX];
            dTemp  = c * ((right - temp) / pow(width, 2)) + 
                     c * ((-temp + bottom) / pow(height, 2));
            u[num] = u[num] + dTemp * dTime;
            return;
        }
        if((num + 1) == nX){
            left   = u[num - 1];
            bottom = u[num + nX];
            dTemp = c * ((-temp + left) / pow(width, 2)) +
                    c * ((-temp + bottom) / pow(height, 2));
            u[num] = u[num] + dTemp * dTime;
            return;
        }
        right  = u[num + 1];
        left   = u[num - 1];
        bottom = u[num + nX];
        dTemp  = c * ((right - 2 * temp + left) / pow(width, 2)) +
                 c * ((-temp + bottom) / pow(height, 2));
        u[num] = u[num] + dTemp * dTime;
        return;
    }
    if((num + 1) > (nY * nX - nX)){
        if((num + 1) == (nY * nX - nX + 1)){
            right  = u[num + 1];
            top    = u[num - nX];
            dTemp = c * ((right - temp) / pow(width, 2)) +
                    c * ((top - temp) / pow(height, 2));
            u[num] = u[num] + dTemp * dTime;
            return;
        }
        if((num + 1) == (nX * nY)){
            top    = u[num - nX];
            left   = u[num - 1];
            dTemp = c * ((-temp + left) / pow(width, 2)) +
                    c * ((top - temp) / pow(height, 2));
            u[num] = u[num] + dTemp * dTime;
            return;
        }
        top    = u[num - nX];
        left   = u[num - 1];
        right  = u[num + 1];
        dTemp = c * ((right - 2 * temp + left) / pow(width, 2)) +\
                c * ((top - temp) / pow(height, 2));
        u[num] = u[num] + dTemp * dTime;
        return;
    }
    if(((num + 1) % nX) == 1){
        top    = u[num - nX];
        right  = u[num + 1];
        bottom = u[num + nX];
        dTemp = c * ((right - temp) / pow(width, 2)) +
                c * ((top - 2 * temp + bottom) / pow(height, 2));
        u[num] = u[num] + dTemp * dTime;
        return;
    }
    if(((num + 1) % nX) == 0){
        left   = u[num - 1];
        top    = u[num - nX];
        bottom = u[num + nX];
        dTemp = c * ((-temp + left) / pow(width, 2)) +
                c * ((top - 2 * temp + bottom) / pow(height, 2));
        u[num] = u[num] + dTemp * dTime;
        return;
    }
    right  = u[num + 1];
    left   = u[num - 1];
    top    = u[num - nX];
    bottom = u[num + nX];
    dTemp = c * ((right - 2 * temp + left) / pow(width, 2)) +
            c * ((top - 2 * temp + bottom) / pow(height, 2));
    u[num] = u[num] + dTemp * dTime;
    return;
}
