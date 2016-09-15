REGISTER '$HOME/useful-macros/pig/coo_matrix/coo_matrix.py' using jython as utils_coo_matrix;

DEFINE COO_MATRIX(data, header_tup, blacklist_tup) RETURNS OUT {
    LA = FOREACH $data GENERATE $0;
    LB = GROUP LA ALL;
    LC = FOREACH LB {
            dis_values = DISTINCT $1;

            GENERATE utils_coo_matrix.getMappingColumns(dis_values, '$blacklist_tup') AS mapping,
                    utils_coo_matrix.getHeader(dis_values, '$header_tup', '$blacklist_tup') AS header,
                    1 AS fake_data;
    }

    LD = GROUP $data BY ($2..);
    LE = FOREACH LD GENERATE $1.($0, $1) AS tup, 1 AS fake_data, group AS dim;

    LF = JOIN LE BY fake_data, LC BY fake_data;
    LG = FOREACH LF GENERATE 1 AS rnk, FLATTEN(dim), utils_coo_matrix.getMatrix(mapping, tup) AS cols;

    LI = FOREACH LC GENERATE 0 AS rnk, header;
    LJ = LIMIT LI 1;

    LK = UNION LJ, LG;
    LL = ORDER LK BY $0 ASC;
    $OUT = FOREACH LL GENERATE $1..;
};
