#!/bin/bash
celery -A wpcs worker --loglevel=info 
celery -A wpcs beat --loglevel=info 