__global__ void check_capacity(float *v1, float *v2, int *s, int *cap){
    int index = blockIdx.x * blockDim.x + threadIdx.x;
    if(
        (s[index] == 1) ||
        (s[index] == 2) ||
        (s[index] == 3)
        ){
            if((v1[index] + v2[index]) > cap[index]){
                s[index] = 0;
            }
    }
}

__global__ void updateV(
        SDL_Rect *cells, 
        float *u1, 
        float *u2, 
        float *u3, 
        float *v, 
        int t, 
        int *s, 
        float *c, 
        float *m,
        int nX, 
        int nY, 
        float dTime
    ){
    int index = blockIdx.x * blockDim.x + threadIdx.x;
    int cT = 1;
    float rightU1, bottomU1, leftU1, topU1;
    float rightU2, bottomU2, leftU2, topU2;
    float rightU3, bottomU3, leftU3, topU3;
    float 
        uT1 = u1[index], 
        uT2 = u2[index], 
        uT3 = u3[index], 
        vT = v[index], 
        dTemp, 
        dV;
    float rightV, bottomV, leftV, topV;
    int width = cells[index].w, height = cells[index].h;
    if(s[index] != 0){
        if(s[index] == t){
            v[index] = 1000;
           return;
         }
    }
    if(index < nX){
        if(index == 0){
            rightU1  = u1[index + 1];
            bottomU1 = u1[index + nX];
            rightU2  = u2[index + 1];
            bottomU2 = u2[index + nX];
            rightU3  = u3[index + 1];
            bottomU3 = u3[index + nX];
            rightV  = v[index + 1];
            bottomV = v[index + nX];
            dV = cT * ((rightV - vT) / pow(width, 2)) +
                 cT * ((-vT + bottomV) / pow(height, 2));
            if(dV == 0){
                return;
            }
            dTemp = dV -
                    c[0] * ((rightU1 - uT1) / pow(width, 2)) -
                    c[0] * ((-uT1 + bottomU1) / pow(height, 2)) -
                    c[1] * ((rightU2 - uT2) / pow(width, 2)) -
                    c[1] * ((-uT2 + bottomU2) / pow(height, 2)) -
                    c[2] * ((rightU3 - uT3) / pow(width, 2)) -
                    c[2] * ((-uT3 + bottomU3) / pow(height, 2));
            float newV = v[index] + dTemp * dTime;
            if(newV < 0){
                v[index] = 0.0f;
                return;
            }
            if((s[index] == 1) || (s[index] == 2) || (s[index] == 3)){
                m[index] = m[index] + newV;
                v[index] = 0;
                return;
            }
            v[index] = newV;
            return;
        }
        if((index + 1) == nX){
            leftU1   = u1[index - 1];
            bottomU1 = u1[index + nX];
            leftU2   = u2[index - 1];
            bottomU2 = u2[index + nX];
            leftU3   = u3[index - 1];
            bottomU3 = u3[index + nX];
            leftV   = v[index - 1];
            bottomV = v[index + nX];
            dV = cT * ((-vT + leftV) / pow(width, 2)) + 
                 cT * ((-vT + bottomV) / pow(height, 2));
            if(dV == 0){
                return;
            }
            dTemp = dV -
                    c[0] * ((-uT1 + leftU1) / pow(width, 2)) - 
                    c[0] * ((-uT1 + bottomU1) / pow(height, 2)) -
                    c[1] * ((-uT2 + leftU2) / pow(width, 2)) - 
                    c[1] * ((-uT2 + bottomU2) / pow(height, 2)) -
                    c[2] * ((-uT3 + leftU3) / pow(width, 2)) - 
                    c[2] * ((-uT3 + bottomU3) / pow(height, 2));
            float newV = v[index] + dTemp * dTime;
            if(newV < 0){
                v[index] = 0.0f;
                return;
            }
            if((s[index] == 1) || (s[index] == 2) || (s[index] == 3)){
                m[index] = m[index] + newV;
                v[index] = 0;
                return;
            }
            v[index] = newV;
            return;
        }
        rightU1  = u1[index + 1];
        leftU1   = u1[index - 1];
        bottomU1 = u1[index + nX];
        rightU2  = u2[index + 1];
        leftU2   = u2[index - 1];
        bottomU2 = u2[index + nX];
        rightU3  = u3[index + 1];
        leftU3   = u3[index - 1];
        bottomU3 = u3[index + nX];
        rightV  = v[index + 1];
        leftV   = v[index - 1];
        bottomV = v[index + nX];
        dV = cT * ((rightV - 2 * vT + leftV) / pow(width, 2)) +
             cT * ((-vT + bottomV) / pow(height, 2));
        if(dV == 0){
            return;
        }
        dTemp = dV -
                c[0] * ((rightU1 - 2 * uT1 + leftU1) / pow(width, 2)) -
                c[0] * ((-uT1 + bottomU1) / pow(height, 2)) -
                c[1] * ((rightU2 - 2 * uT2 + leftU2) / pow(width, 2)) -
                c[1] * ((-uT2 + bottomU2) / pow(height, 2)) -
                c[2] * ((rightU3 - 2 * uT3 + leftU3) / pow(width, 2)) -
                c[2] * ((-uT3 + bottomU3) / pow(height, 2)) ;
        float newV = v[index] + dTemp * dTime;
        if(newV < 0){
            v[index] = 0.0f;
            return;
        }
        if((s[index] == 1) || (s[index] == 2) || (s[index] == 3)){
            m[index] = m[index] + newV;
            v[index] = 0;
            return;
        }
        v[index] = newV;
        return;
    }
    if((index + 1) > (nY * nX - nX)){
        if((index + 1) == (nY * nX - nX + 1)){
            rightU1  = u1[index + 1];
            topU1    = u1[index - nX];
            rightU2  = u2[index + 1];
            topU2    = u2[index - nX];
            rightU3  = u3[index + 1];
            topU3    = u3[index - nX];
            rightV  = v[index + 1];
            topV    = v[index - nX];
            dV = dTemp = cT * ((rightV - vT) / pow(width, 2)) + 
                    cT * ((topV - vT) / pow(height, 2));
            if(dV == 0){
                return;
            }
            dTemp = dV -
                    c[0] * ((rightU1 - uT1) / pow(width, 2)) - 
                    c[0] * ((topU1 - uT1) / pow(height, 2)) - 
                    c[1] * ((rightU2 - uT2) / pow(width, 2)) - 
                    c[1] * ((topU2 - uT2) / pow(height, 2)) -
                    c[2] * ((rightU3 - uT3) / pow(width, 2)) - 
                    c[2] * ((topU3 - uT3) / pow(height, 2));
            float newV = v[index] + dTemp * dTime;
            if(newV < 0){    
                v[index] = 0.0f;
                return;
            }
            if((s[index] == 1) || (s[index] == 2) || (s[index] == 3)){
                m[index] = m[index] + newV;
                v[index] = 0;
                return;
            }
            v[index] = newV;
            return;
        }
        if((index + 1) == (nX * nY)){
            topU1    = u1[index - nX];
            leftU1   = u1[index - 1];
            topU2    = u2[index - nX];
            leftU2   = u2[index - 1];
            topU3    = u3[index - nX];
            leftU3   = u3[index - 1];
            leftV   = v[index - 1];
            topV    = v[index - nX];
            dV = cT * ((-vT + leftV) / pow(width, 2)) + 
                 cT * ((topV - vT) / pow(height, 2));
            if(dV == 0){
                return;
            }
            dTemp = dV -
                    c[0] * ((-uT1 + leftU1) / pow(width, 2)) - 
                    c[0] * ((topU1 - uT1) / pow(height, 2)) -
                    c[1] * ((-uT2 + leftU2) / pow(width, 2)) - 
                    c[1] * ((topU2 - uT2) / pow(height, 2)) -
                    c[2] * ((-uT3 + leftU3) / pow(width, 2)) - 
                    c[2] * ((topU3 - uT3) / pow(height, 2));
            float newV = v[index] + dTemp * dTime;
            if(newV < 0){    
                v[index] = 0.0f;
                return;
            }
            if((s[index] == 1) || (s[index] == 2) || (s[index] == 3)){
                m[index] = m[index] + newV;
                v[index] = 0;
                return;
            }
            v[index] = newV;
            return;
        }
        topU1    = u1[index - nX];
        leftU1   = u1[index - 1];
        rightU1  = u1[index + 1];
        topU2    = u2[index - nX];
        leftU2   = u2[index - 1];
        rightU2  = u2[index + 1];
        topU3    = u3[index - nX];
        leftU3   = u3[index - 1];
        rightU3  = u3[index + 1];
        rightV  = v[index + 1];
        leftV   = v[index - 1];
        topV    = v[index - nX];
        dV = cT * ((rightV - 2 * vT + leftV) / pow(width, 2)) + 
             cT * ((topV - vT) / pow(height, 2));
        if(dV == 0){
            return;
        }
        dTemp = dV -
                c[0] * ((rightU1 - 2 * uT1 + leftU1) / pow(width, 2)) - 
                c[0] * ((topU1 - uT1) / pow(height, 2)) - 
                c[1] * ((rightU2 - 2 * uT2 + leftU2) / pow(width, 2)) - 
                c[1] * ((topU2 - uT2) / pow(height, 2)) -
                c[2] * ((rightU3 - 2 * uT3 + leftU3) / pow(width, 2)) - 
                c[2] * ((topU3 - uT3) / pow(height, 2));
        float newV = v[index] + dTemp * dTime;
        if(newV < 0){
            v[index] = 0.0f;
            return;
        }
        if((s[index] == 1) || (s[index] == 2) || (s[index] == 3)){
            m[index] = m[index] + newV;
            v[index] = 0;
            return;
        }
        v[index] = newV;
        return;
    }
    if(((index + 1) % nX) == 1){
        topU1    = u1[index - nX];
        rightU1  = u1[index + 1];
        bottomU1 = u1[index + nX];
        topU2    = u2[index - nX];
        rightU2  = u2[index + 1];
        bottomU2 = u2[index + nX];
        topU3    = u3[index - nX];
        rightU3  = u3[index + 1];
        bottomU3 = u3[index + nX];
        rightV  = v[index + 1];
        topV    = v[index - nX];
        bottomV = v[index + nX];
        dV = cT * ((rightV - vT) / pow(width, 2)) + 
             cT * ((topV - 2 * vT + bottomV) / pow(height, 2));
        if(dV == 0){
            return;
        }
        dTemp = dV -
                c[0] * ((rightU1 - uT1) / pow(width, 2)) -
                c[0] * ((topU1 - 2 * uT1 + bottomU1) / pow(height, 2)) -
                c[1] * ((rightU2 - uT2) / pow(width, 2)) -
                c[1] * ((topU2 - 2 * uT2 + bottomU2) / pow(height, 2)) -
                c[2] * ((rightU3 - uT3) / pow(width, 2)) -
                c[2] * ((topU3 - 2 * uT3 + bottomU3) / pow(height, 2));
        float newV = v[index] + dTemp * dTime;
        if(newV < 0){
            v[index] = 0.0f;
            return;
        }
        if((s[index] == 1) || (s[index] == 2) || (s[index] == 3)){
            m[index] = m[index] + newV;
            v[index] = 0;
            return;
        }
        v[index] = newV;
        return;
    }
    if(((index + 1) % nX) == 0){
        leftU1   = u1[index - 1];
        topU1    = u1[index - nX];
        bottomU1 = u1[index + nX];
        leftU2   = u2[index - 1];
        topU2    = u2[index - nX];
        bottomU2 = u2[index + nX];
        leftU3   = u3[index - 1];
        topU3    = u3[index - nX];
        bottomU3 = u3[index + nX];
        leftV   = v[index - 1];
        topV    = v[index - nX];
        bottomV = v[index + nX];
        dV = cT * ((-vT + leftV) / pow(width, 2)) +
             cT * ((topV - 2 * vT + bottomV) / pow(height, 2));
        if(dV == 0){
            return;
        }
        dTemp = dV -
                c[0] * ((-uT1 + leftU1) / pow(width, 2)) -
                c[0] * ((topU1 - 2 * uT1 + bottomU1) / pow(height, 2)) -
                c[1] * ((-uT2 + leftU2) / pow(width, 2)) -
                c[1] * ((topU2 - 2 * uT2 + bottomU2) / pow(height, 2)) -
                c[2] * ((-uT3 + leftU3) / pow(width, 2)) -
                c[2] * ((topU3 - 2 * uT3 + bottomU3) / pow(height, 2));
        float newV = v[index] + dTemp * dTime;
        if(newV < 0){
            v[index] = 0.0f;
            return;
        }
        if((s[index] == 1) || (s[index] == 2) || (s[index] == 3)){
            m[index] = m[index] + newV;
            v[index] = 0;
            return;
        }
        v[index] = newV;
        return;
    }
    rightU1  = u1[index + 1];
    leftU1   = u1[index - 1];
    topU1    = u1[index - nX];
    bottomU1 = u1[index + nX];
    rightU2  = u2[index + 1];
    leftU2   = u2[index - 1];
    topU2    = u2[index - nX];
    bottomU2 = u2[index + nX];
    rightU3  = u3[index + 1];
    leftU3   = u3[index - 1];
    topU3    = u3[index - nX];
    bottomU3 = u3[index + nX];
    rightV  = v[index + 1];
    leftV   = v[index - 1];
    topV    = v[index - nX];
    bottomV = v[index + nX];
    dV = cT * ((rightV - 2 * vT + leftV) / pow(width, 2)) + 
         cT * ((topV - 2 * vT + bottomV) / pow(height, 2));
    if(dV == 0){
        return;
    }
    dTemp = dV -
            c[0] * ((rightU1 - 2 * uT1 + leftU1) / pow(width, 2)) - 
            c[0] * ((topU1 - 2 * uT1 + bottomU1) / pow(height, 2)) -
            c[1] * ((rightU2 - 2 * uT2 + leftU2) / pow(width, 2)) - 
            c[1] * ((topU2 - 2 * uT2 + bottomU2) / pow(height, 2)) -
            c[2] * ((rightU3 - 2 * uT3 + leftU3) / pow(width, 2)) - 
            c[2] * ((topU3 - 2 * uT3 + bottomU3) / pow(height, 2));
    float newV = v[index] + dTemp * dTime;
    if(newV < 0){
        v[index] = 0.0f;
        return;
    }
    if((s[index] == 1) || (s[index] == 2) || (s[index] == 3)){
            m[index] = m[index] + newV;
            v[index] = 0;
            return;
        }
        v[index] = newV;
    return;
}

__global__ void updateU(SDL_Rect * cells, float *u, int t, int *s, float c, int nX, int nY, float dTime){
    int index = blockIdx.x * blockDim.x + threadIdx.x;
    float right, bottom, left, top, temp = u[index], dTemp;
    int width = cells[index].w, height = cells[index].h;
    if(s[index] != 0){
        if(s[index] == t){
            u[index] = 1000;
            return;
        }
    }
    if(index < nX){
        if(index == 0){
            right  = u[index + 1];
            bottom = u[index + nX];
            dTemp  = c * ((right - temp) / pow(width, 2)) + 
                     c * ((-temp + bottom) / pow(height, 2));
            u[index] = u[index] + dTemp * dTime;
            return;
        }
        if((index + 1) == nX){
            left   = u[index - 1];
            bottom = u[index + nX];
            dTemp = c * ((-temp + left) / pow(width, 2)) +
                    c * ((-temp + bottom) / pow(height, 2));
            u[index] = u[index] + dTemp * dTime;
            return;
        }
        right  = u[index + 1];
        left   = u[index - 1];
        bottom = u[index + nX];
        dTemp  = c * ((right - 2 * temp + left) / pow(width, 2)) +
                 c * ((-temp + bottom) / pow(height, 2));
        u[index] = u[index] + dTemp * dTime;
        return;
    }
    if((index + 1) > (nY * nX - nX)){
        if((index + 1) == (nY * nX - nX + 1)){
            right  = u[index + 1];
            top    = u[index - nX];
            dTemp = c * ((right - temp) / pow(width, 2)) +
                    c * ((top - temp) / pow(height, 2));
            u[index] = u[index] + dTemp * dTime;
            return;
        }
        if((index + 1) == (nX * nY)){
            top    = u[index - nX];
            left   = u[index - 1];
            dTemp = c * ((-temp + left) / pow(width, 2)) +
                    c * ((top - temp) / pow(height, 2));
            u[index] = u[index] + dTemp * dTime;
            return;
        }
        top    = u[index - nX];
        left   = u[index - 1];
        right  = u[index + 1];
        dTemp = c * ((right - 2 * temp + left) / pow(width, 2)) +\
                c * ((top - temp) / pow(height, 2));
        u[index] = u[index] + dTemp * dTime;
        return;
    }
    if(((index + 1) % nX) == 1){
        top    = u[index - nX];
        right  = u[index + 1];
        bottom = u[index + nX];
        dTemp = c * ((right - temp) / pow(width, 2)) +
                c * ((top - 2 * temp + bottom) / pow(height, 2));
        u[index] = u[index] + dTemp * dTime;
        return;
    }
    if(((index + 1) % nX) == 0){
        left   = u[index - 1];
        top    = u[index - nX];
        bottom = u[index + nX];
        dTemp = c * ((-temp + left) / pow(width, 2)) +
                c * ((top - 2 * temp + bottom) / pow(height, 2));
        u[index] = u[index] + dTemp * dTime;
        return;
    }
    right  = u[index + 1];
    left   = u[index - 1];
    top    = u[index - nX];
    bottom = u[index + nX];
    dTemp = c * ((right - 2 * temp + left) / pow(width, 2)) +
            c * ((top - 2 * temp + bottom) / pow(height, 2));
    u[index] = u[index] + dTemp * dTime;
    return;
}
