FILES :=                              \
    .travis.yml                       \
    apiary.apib                       \
    makefile                          \
    IDB1.log                          \
    models.html                       \
    app/models.py                     \
    app/tests.py                      \
    app/summoners.txt                 \
    app/requirements.txt              \
    app/teams.txt                     \
    app/champions.txt                 \
    run_local.sh                      \
    push_to_prod.sh                   \
    docker-compose-prod.yml           \
    docker-compose-common.yml         \
    docker-compose.yml                \
    scraping/api_scrape.py            \
    UML.pdf                           \

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  *.pyc
	rm -rf __pycache__

config:
	git config -l

scrub:
	make clean
	rm -f  models.html
	rm -f  IDB1.log
	rm -rf tests.py

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: 
	coverage run app/tests.py 
	coverage report --include=app/test_models.py,app/tests.py

model.html: models.py
	pydoc3 -w models

IDB1.log:
	git log > IDB1.log
