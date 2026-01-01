from itertools import *

def find_divisors(n):
    if n == 0:
        return []

    n = abs(n)
    divs = [1, n]
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n // i: divs.append(round(n // i))

    all_divs = divs + [-d for d in divs]
    sorted(all_divs)
    return all_divs

####################################################################################

def generate_combinations(points, pow, k):
    result = []

    # выбираем все возможные комбинации k массивов
    for selected_indexes in combinations(range(pow), k):
        selected_points_arrays = [points[i] for i in selected_indexes]

        # генерируем декартово произведение выбранных массивов
        combs = list(product(*selected_points_arrays))
        result.extend(combs)

    return result


def get_all_combinations(points, pow):
    result = {}

    for k in range(2, pow+1):
        result[k] = generate_combinations(points, pow, k)

    return result

####################################################################################

def is_polynomial(p):
    f = True
    if p[-1] == 0 or len(p) == 1: f=False
    return f

def get_polynomial_value(polynomial, x):
    result = 0
    for i in range(len(polynomial)): result += polynomial[i] * x ** i
    return result

def multiply_polynomials(p, q):
    result = []

    for i in range(len(p)):
        for j in range(len(q)):
            if len(result) - 1 < i + j:
                result.append(p[i] * q[j])
            else:
                result[i + j] += p[i] * q[j]

    return result


def divide_polynomials(p, q):
    result = []

    pi = len(p) - 1
    qi = len(q) - 1
    while pi >= qi:
        multi = p[pi] / q[qi]
        result.insert(0, multi)
        for i, j in zip(range(pi, pi - qi - 1, -1), range(qi, -1, -1)):
            p[i] -= multi * q[j]
        pi -= 1

    return result, p

def print_polynomial_ver_1_2(p):
    if not p:
        return "0"

    result = ""
    for i in range(len(p) - 1, -1, -1):
        if p[i] != 0:
            k = str(abs(p[i]))
            if abs(p[i]) == 1 and i != 0:
                k = ''

            if i == 0: result += k
            elif i == 1: result += k + 'x'
            else: result += k + 'x^' + str(i)

            if i != 0:
                if i > 0:
                    # Проверяем следующий коэффициент
                    next_nonzero = False
                    for j in range(i - 1, -1, -1):
                        if p[j] != 0:
                            next_nonzero = True
                            if p[j] > 0: result += ' + '
                            else: result += ' - '
                            break
    if result == "":
        result = "0"

    return result

####################################################################################

def get_coefficients(x, y):
    k = []
    for i in range(0, len(x)):
        temp = y[i]
        for j in range(0, len(x)):
            if i != j:
                temp *= (1 / (x[i] - x[j]))
        k.append(temp)
    return k

count_lagrange = 0

def get_lagrange_polynomial(x, y, n, initial):
    global count_lagrange
    count_lagrange += 1

    monomials = []
    for i in range(0, len(x)):
        monomials.append([-x[i], 1])

    multipliers_order = combinations(monomials, n-1)

    l_polys = []
    for m in multipliers_order:
        v = m[0]
        if n > 2:
            for j in range(1, len(m)):
                v = multiply_polynomials(v, m[j])
        l_polys.insert(0, v)

    k = get_coefficients(x, y)
    answer = [0 for i in range(n)]
    for i in range(len(l_polys)):
        for j in range(n):
            answer[j] += l_polys[i][j] * k[i]

    # проверка целостности коэффициентов
    check = True
    if is_polynomial(answer):
        for aa in answer:
            if aa != int(aa):
                check = False
                break
    else:
        check = False

    if check:
        answer = [round(coef) for coef in answer]
        initial_copy = initial.copy()
        p, q = divide_polynomials(initial_copy, answer)

        f = True
        for qq in q:
            if qq != 0:
                f = False
                break

        if f:
            return answer

    return [0]

####################################################################################

def kronecker_factorization_ver_1_2(polynomial):
    global count_lagrange
    count_lagrange = 0

    original_poly = polynomial.copy()
    factorization = []

    # a = 0,1,-1,2,-2 ... без сортировки
    while is_polynomial(polynomial):
        # m + 1
        n = len(polynomial) - 1
        m = n // 2 + 1

        # находим точки, массив a и сразу значения в массиве values
        a = []
        values = []
        a_i = 0
        mm = 0
        while mm < m:
            a.append(a_i)
            values.append(get_polynomial_value(polynomial, a_i))
            mm+=1
            if a_i != 0:
                a.append(-a_i)
                values.append(get_polynomial_value(polynomial, -a_i))
                mm+=1
            a_i+=1

        # делители для каждого значения
        divs = [find_divisors(v) for v in values]

        # трехмерный массив точек
        points = [[] for i in range(len(divs))]

        for i in range(len(divs)):
            for j in range(len(divs[i])):
                temp = [a[i], divs[i][j]]
                points[i].append(temp)

        # генерация все декартовы произведения
        combs_in_dict = get_all_combinations(points, m)
        combs = [combs_in_dict[i][j] for i in combs_in_dict.keys() for j in range(len(combs_in_dict[i]))]

        found = False
        for i in range(len(combs)):
            x = []
            y = []

            for point in combs[i]:
                x.append(point[0])
                y.append(point[1])

            p = get_lagrange_polynomial(x, y, len(combs[i]), polynomial)
            if is_polynomial(p):
                found = True
                if p[-1] < 0: p = [-1*round(pp) for pp in p]
                else: p = [round(pp) for pp in p]
                factorization.append(p)
                polynomial, q = divide_polynomials(polynomial, p)
                polynomial = [round(pp) for pp in polynomial]
                break

        # этот многочлен неприводим
        if not found:
            p = polynomial.copy()
            p = [round(pp) for pp in p]
            factorization.append(p)
            polynomial = [0]

    return {
            "original": original_poly,
            "factorization": factorization,
            "lagrange_count": count_lagrange
        }