Send a pdf to a Mail Adress and automatically get a splitted PDF with custom splitpoints and filenames.

1. run postla.py
2. send a mail to batla@gmx.at with your desired splitting points in the subject

you can also use the sendmail.sh script to send a mail with a testpdf using "mutt"


How to format the subject:
- start the subject with "pdf" followed by space
- then enter "{first splitpoint as number}{underscore}{filename of pdf}
- then enter second splitpoint with same format divided by space and so on

e.g. Subject:
"pdf 3_untilthree 6_untilsix 9_untilnine"
creates 3 pdf:
- untilthree.pdf (page 1 until 3)
- untilsix.pdf (page 4 until 6)
- untilnine.pdf (page 7 until 9)


