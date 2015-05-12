import json
import argparse
import numpy as np


def load_grades_file(filename):
    with open(filename) as f:
        return json.loads(f.read())


def sum_credits(grades, key):
    completed = grades[key]
    credit_sum = 0
    for _, grade in completed.iteritems():
        credit_sum += grade["credit"]
    return credit_sum


def calculate_completed_average(grades):
    completed = grades["completed"]
    credit_sum = sum_credits(grades, "completed")
    avg = 0.0
    for _, grade in completed.iteritems():
        avg += float(grade["grade"]) * grade["credit"] / credit_sum
    return avg


def calculate_needed_average(grades, goal):
    lcs = sum_credits(grades, "left")
    ccs = sum_credits(grades, "completed")
    ts = lcs + ccs
    ca = calculate_completed_average(grades)
    return ts * (goal - (ca * ccs / ts)) / lcs


def calculate_needed_grades(grades, goal):
    na = calculate_needed_average(grades, goal)
    left = grades["left"]
    exam_grades = dict()
    for name, grade in left.iteritems():
        gr = float(grade["grade"])
        w = grade["weight"]
        eg = (na - gr * w) / (1 - w)
        exam_grades[name] = eg
    return exam_grades


def get_overall_grades(grades, needed):
    results = list()
    for _, grade in grades["completed"].iteritems():
        if grade["credit"] == 15:
            results.append(grade["grade"])
        if grade["credit"] == 30:
            results.append(grade["grade"])
            results.append(grade["grade"])

    for name, grade in needed.iteritems():
        left_gr = grades["left"][name]["grade"]
        left_w = grades["left"][name]["weight"]
        results.append(left_gr * left_w + (1 - left_w) * grade)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Calculates the grades you need, if the results \
        are negative or over 20, you cant get those grades. Too lazy \
        to make it better just deal with it."
    )
    parser.add_argument(
        "--goal", dest="goal", type=float, default=16.5,
        help="Your goal for your overall mark."
    )
    parser.add_argument(
        "--grades", dest="grades", type=str, default="grades.json",
        help="JSON file containing your current grades"
    )
    args = parser.parse_args()
    grades = load_grades_file(args.grades)
    egs = calculate_needed_grades(grades, args.goal)
    o_grades = get_overall_grades(grades, egs)
    print "Median :", np.median(o_grades)
    print "Mean : ", np.mean(o_grades)
    for name, eg in egs.iteritems():
        print name, ":", eg


if __name__ == "__main__":
    main()
