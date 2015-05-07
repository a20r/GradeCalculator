
import json
import argparse


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


def get_goal(goal_str):
    goal_str = goal_str.lower()
    if goal_str == "first" or goal_str == "1":
        goal = 16.5
    elif goal_str == "2.1":
        goal = 13.5
    elif goal_str == "2.2":
        goal = 10.5
    else:
        goal = float(goal_str)
    return goal


def main():
    parser = argparse.ArgumentParser(
        description="Calculates the grades you need, if the results \
        are negative or over 20, you cant get those grades. Too lazy \
        to make it better just deal with it. Also I don't support \
        classifications under 2.2, so you will just have to enter \
        the goal yourself."
    )
    parser.add_argument(
        "--goal", dest="goal", type=str, default="16.5",
        help="Your goal for your overall mark, either a classification \
        or a actual average. Acceptable formats: 17, 2.1, First, etc"
    )
    parser.add_argument(
        "--grades", dest="grades", type=str, default="grades.json",
        help="JSON file containing your current grades"
    )
    args = parser.parse_args()
    grades = load_grades_file(args.grades)
    goal = get_goal(args.goal)
    egs = calculate_needed_grades(grades, goal)
    for name, eg in egs.iteritems():
        print name, ":", eg


if __name__ == "__main__":
    main()
