#!/bin/bash
# Cron job script to run the timetable automation

# Log file for cron output
LOG_FILE="/app/cron.log"

# Run the main script
echo "========================================" >> $LOG_FILE
echo "Cron job started at $(date)" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

cd /app
python3 main.py >> $LOG_FILE 2>&1

echo "Cron job completed at $(date)" >> $LOG_FILE
echo "" >> $LOG_FILE
