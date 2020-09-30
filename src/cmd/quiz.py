# quiz command

import common

def quiz(update, context, qs=2):

    info = get_user_info(update)
    info["quizs"] = info["quizs"] + 1
    set_user_info(update, info)

    # extract keyword text
    keyword = cmd_tail(upadate)
    
    q = build_heading_quiz(qs, keyword=keyword, sources_subset=info["sources"])
    if not q:
        q = build_default_quiz()
        
    questions = q["sources"]
    prefix = "Where was this heading published?\n\n"  if info["quizs"] <= 3 else ""
    message = update.effective_message.reply_poll(prefix + q["title"],
                                                  questions, type=Poll.QUIZ, correct_option_id=q["index"])
    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    payload = {message.poll.id: {"chat_id": update.effective_chat.id,
                                 "message_id": message.message_id,
                                 "q": q,
                                 "qs": qs}}
    context.bot_data.update(payload)

def quiz_post_timer(context):
    quiz_data = context.job.context
    msg = ""
    if quiz_data["q"]["link"]:
        msg += quiz_data["q"]["link"] + "\n\n"
    context.bot.send_message(quiz_data["chat_id"], text=msg + "/quiz, /quiz3, /quiz4 or /help")  
            

def receive_quiz_answer(update, context):
    # the bot can receive closed poll updates we don't care about
    if update.poll.is_closed:
        return
    if update.poll.total_voter_count == 3:
        try:
            quiz_data = context.bot_data[update.poll.id]
        # this means this poll answer update is from an old poll, we can't stop it then
        except KeyError:
            return
        context.bot.stop_poll(quiz_data["chat_id"], quiz_data["message_id"])
        
    if update.poll:
        quiz_data = context.bot_data[update.poll.id]
        chat_id = quiz_data["chat_id"]
        new_job = context.job_queue.run_once(quiz_post_timer, 2, context=quiz_data)
