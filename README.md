# GradeCalculator
Calculating your remaining grades so you don't have to 

# Running
    python calculator.py --grades=[your grades.json file] --goal=[your goal grade overall]

# Help
    $ python calculator.py --help
    usage: calculator.py [-h] [--goal GOAL] [--grades GRADES]

    Calculates the grades you need, if the results are negative or over 20, you
    cant get those grades. Too lazy to make it better just deal with it. Also I
    don't support classifications under 2.2, so you will just have to enter the
    goal yourself.

    optional arguments:
    -h, --help       show this help message and exit
    --goal GOAL      Your goal for your overall mark, either a classification or
                    a actual average. Acceptable formats: 17, 2.1, First, etc
    --grades GRADES  JSON file containing your current grades


# Example
    $ python calculator.py --grades=grades.json --goal=16.5
    CP : 12.3555555556
    DM : 11.2222222222
    DS : 12.7555555556

