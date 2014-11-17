MLProject
=========

50.007 Machine Learning Project

1 Part 1 (20 points)
Recall that the HMM discussed in class is defined as follows:
p( x 1 , . . . , xn, y 1, . . . , yn) =
n +1
Yi
=1
q(yi|yi − 1) ·
n Yi
=1
e(xi|yi) (1)
where y 0 = ∗ and yn +1 = STOP. Here q are transition probabilities, and e are emission parameters.
• (5 pts) Write a function that estimates the emission parameters from the training set using MLE
(maximum likelihood estimation):
e(x|y) = Count(y → x)
Count(y)
• (5 pts) One problem with estimating the emission parameters is that some words that appear in the
test set do not appear in the training set. One simple idea is to assign a fixed probability to all such
new words. For example, we can simply do the following:
– If x is a new word (that did not appear in the training set):
1
Count(y) + 1
2
– If x appeared in the training set:
Count(y → x)
Count(y) + 1
for any x and y. Implement this fix into your function for computing the emission parameters.
• (10 pts) Implement a simple POS tagger that produces the tag
y ∗ = argmax
y
e(x |y)
for each word x in the sequence.
Learn these parameters with train, and evaluate your system on the development set dev.in.
Write your output to dev.p1.out. Compare your outputs and the gold-standard outputs in dev.out
and report the accuracy score of such a baseline system. The accuracy score is defined as follows:
Accuracy =
Total number of correctly predicted POS tags
Total number of predicted POS tags
2 Part 2 (20 points)
• (5 pts) Write a function that estimates the transition parameters from the training set using MLE
(maximum likelihood estimation):
q(yi|yi − 1) = Count(yi − 1, yi)
Count(yi − 1)
Please make sure the following special cases are also considered: q(STOP|yn) and q(y 1|∗).
• (15 pts) Use the estimated transition and emission parameters, implement the Viterbi algorithm to
compute the following:
y 1∗, . . . , yn∗ = argmax
y 1 ,...,y n
p(x 1, . . . , xn, y 1, . . . , yn)
Run the Viterbi algorithm on the development set dev.in. Write your output to dev.p2.out.
Report the accuracy score of this POS tagging system.
Note that you might encounter potential numerical underflow issue. Think of a way to address such
an issue in your implementation.
3 Part 3 – Challenge (10 points)
• (5 pts) Now, based on the training and development set, think of a better design for developing an
improved POS tagger for tweets using the hidden Markov model. You are not allowed to use any
external resources or packages. Note that you must design your new POS tagger within the framework
of the hidden Markov model but you are free to perform any automatic preprocessing of the data.
Please run your system on the development set dev.in. Write your outputs to dev.p3.out.
Report the accuracy score of your new system.
3
• (5 pts) We will evaluate your system’s performance on a held out test set test.in. The test set
will only be released on 9 Dec 2014 at 5pm (48 hours before the deadline). Use your new system to
generate the output POS tags. Write your output to test.p3.out.
The system that achieves the highest accuracy on the test set will be announced as the winner.
Hints: Are there better ways to handle new words? Are there better ways to model the transition probabilities? Are there linguistic patterns associated with words? Can we cluster words into semantic classes?
Any other ideas?
