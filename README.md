##### Desired Features



* ###### user authentication system

  * \[DONE] login \& logout
  * \[DONE] change password
  * \[DONE] sending email
  * \[DONE] reset password
  * login using email



* ###### user registration

  * \[DONE] Email verification
  * \[DONE] Avoid inserting repetitive email
  * Rate limiting



##### Bugs



  * In save() method of NoteCreateView, new category object may be saved in database without considering "if commit == True". Saving multiple related object should be reviewed.

