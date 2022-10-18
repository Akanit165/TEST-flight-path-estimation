clc;
clear;
close all;

syms r_e r mu lat long u;

degree = 1; % Define degree of polynomial
%mu = 3.986e5; % km3s-2
%r_e = 6371; %km


C   =  [       1       0       0       0;
               0       0       0       0;
        -1.08e-3       0 1.57e-6       0;
         2.53e-6 2.18e-6 3.11e-7 1.02e-7];


S   =  [0       0        0       0;
        0       0        0       0;
        0       0 -9.03e-7       0;
        0 2.68e-7 -2.12e-7 1.98e-7];

% =================================================
% satellite acceleration component in r (ECEF)
% =================================================

SUM_M_r = [];
P_LM_r = [];

for l = 0:degree
    
    f_n = (u^2-1)^l;
    p_l = (1/((2^l)*factorial(l)))*diff(f_n,l);
    lr = (l+1)*(r_e/r)^l; % Term depend on l

    for m = 0:l

       p_lmr = (1-u^2)^(m/2)*diff(p_l,m);
       p_lmr = subs(p_lmr,u,sin(lat)); % Substitute u with sin(phi)
       P_LM_r = [P_LM_r ; p_lmr]; % Collect Legendre polynomial for each loop
       
       sum_mr = lr*p_lmr*(C(l+1,m+1)*cos(m*long)+S(l+1,m+1)*sin(m*long));
       
       SUM_M_r = [SUM_M_r sum_mr]; % Collect the multiplication for each loop

    end
end

P_LM_r; % Legendre polynomial in r component
SUM_M_r;

sum_r = sum(SUM_M_r); % Summation in r component

accel_r = (-mu/(r^2))*sum_r % Accel in r component

% =================================================
% satellite acceleration component in phi (ECEF)
% =================================================

SUM_M_p = [];
P_LM_p = [];

for l = 1:degree
    
    f_n = (u^2-1)^l;
    p_n = (1/((2^l)*factorial(l)))*diff(f_n,l);
    lp = (r_e/r)^l;

    for m = 0:l

       p_lmp = (1-u^2)^(m/2)*diff(p_n,m);
       p_lmp = subs(p_lmp,u,sin(lat)); % Substitute u with sin(phi)
       P_LM_p = [P_LM_p ; p_lmp];
       
       sum_mp = lp*diff(p_lmp)*(C(l+1,m+1)*cos(m*long)+S(l+1,m+1)*sin(m*long));
       
       SUM_M_p = [SUM_M_p sum_mp];

    end
end

P_LM_p; % Legendre polynomial in phi component
SUM_M_p;

sum_p = sum(SUM_M_p); % Summation in phi component

accel_phi = (mu/r^2)*sum_p

% =================================================
% satellite acceleration component in lambda (ECEF)
% =================================================

SUM_M_l = [];
P_LM_l = [];

for l = 1:degree
    
    f_n = (u^2-1)^l;
    p_n = (1/((2^l)*factorial(l)))*diff(f_n,l);
    ll = (r_e/r)^l; % Term in summation depend on l
   
    for m = 1:l

       p_lml = (1-u^2)^(m/2)*diff(p_n,m);
       p_lml = subs(p_lml,u,sin(lat)); % Substitute u with sin(phi)
       P_LM_l = [P_LM_l ; p_lml];  
       
       sum_ml = ll*m*(p_lml/cos(lat))*(-C(l+1,m+1)*sin(m*long)+S(l+1,m+1)*cos(m*long));
       
       SUM_M_l = [SUM_M_l sum_ml];

    end
end

P_LM_l; % Legendre polynomial in lambda component
SUM_M_l;

sum_l = sum(SUM_M_l);

accel_lambda = (mu/r^2)*sum_l

% =================================================
% Transform ECEF acceleration in spherical to cartesian 
% =================================================

accel_polar = [accel_r accel_phi accel_lambda];

polar2cat = [cos(lat)*cos(long) -sin(lat)*cos(long) -sin(long);
             cos(lat)*sin(long) -sin(lat)*sin(long)  cos(long);
             sin(lat)            cos(lat)            0];

accel_cat = polar2cat*transpose(accel_polar); % Satellite acceleration in catesian coordinate

% Acceleration in ECEF (Catesian)

a_x = accel_cat(1)
a_y = accel_cat(2)
a_z = accel_cat(3)









