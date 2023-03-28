#!/usr/bin/env bash

# Shell script used as a "Makefile-like" helper tool.
# Usage: Enter ". make.sh key" in the pycharm terminal,
# where "key" is one of the keywords below (e.g. "venv" or "unittest").
# Set up pycharm as described in the PACE_EVA/docs folder to access GitBash
# directly from pycharm terminal.


for KEYWORD in "$@"
do
    case "${KEYWORD}"
    in

        "venv")  # User entered ". make.sh venv"
            # For pycharm users: Activate virtual environment
            source .venv/Scripts/activate
            echo virtual environment activated
            ;;

        "install")  # User entered ". make.sh install"
            # install all modules to .venv (to be used after inital cloning of repo)
            pip install -r install_requirements.txt
            echo virtual environment populated
            ;;

        "env_freeze")  # Dump list of all installed modules to text file
            pip freeze > install_requirements.txt
            echo virtual environment saved to .txt file
            ;;

        "lint")
            # flake8/pylint is a tool for automated code style checks
            flake8 ./data ./map ./scripts
            echo flake8 finished
            ;;

        "test")
            # run python tests
            # Excecutes all sanity check funtions delared in .unittest/ folder
            python -m pytest unittest

            # Usually, all py files in the tests/ folder are run, but this might
            # not work on some of the IDEs ued.
            # python -m pytest
            ;;

        "count_lines")
            # Count all self-written lines of python code within the repository
            # Exclude all files in .gitignore
            git ls-files | grep py | xargs wc -l
            ;;

        *)
            # default action if keyword not recognized, do nothing
            echo Make inactive, no keyword specified
            ;;
    esac
done
