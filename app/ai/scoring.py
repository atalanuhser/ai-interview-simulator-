import json

from app.ai.gemini_client import get_client

from app.ai.prompts import build_scoring_prompt





def normalize_score(score):

"""

Score'u güvenli şekilde 0-10 aralığına çevirir.

"""



try:

score = float(score)

except:

return 0



# Eğer AI yanlışlıkla 100lük sistem verdiyse

if score > 10:

score = score / 10



# Clamp

score = max(0, min(score, 10))



return round(score, 1)





def has_meaningful_answers(qa_history):

"""

Kullanıcı gerçekten cevap vermiş mi kontrol eder.

"""



meaningful_count = 0



for qa in qa_history:

answer = qa.get("answer", "").strip().lower()



if len(answer) > 10 and answer not in [

"hi",

"hello",

"ok",

"yes",

"no",

"idk",

"i don't know",

]:

meaningful_count += 1



return meaningful_count >= 2





def parse_final_scores(final_data: dict, qa_history=None) -> dict:



scores = final_data.get("scores", {})

feedback = final_data.get("feedback", {})



# Eğer kullanıcı düzgün cevap vermediyse skorları düşür

low_quality = False



if qa_history is not None:

low_quality = not has_meaningful_answers(qa_history)



technical = normalize_score(scores.get("technical_competency", 0))

communication = normalize_score(scores.get("communication_skills", 0))

problem_solving = normalize_score(scores.get("problem_solving", 0))

experience_fit = normalize_score(scores.get("experience_fit", 0))

motivation = normalize_score(scores.get("motivation", 0))



# Boş / anlamsız cevaplarda skor düşür

if low_quality:

technical = min(technical, 3)

communication = min(communication, 3)

problem_solving = min(problem_solving, 3)

experience_fit = min(experience_fit, 3)

motivation = min(motivation, 3)



return {

"radar": {

"Technical Competency": technical,

"Communication": communication,

"Problem Solving": problem_solving,

"Experience Fit": experience_fit,

"Motivation": motivation,

},

"overall_comment": feedback.get(

"overall_comment",

"The candidate needs improvement."

),

"strengths": feedback.get("strengths", []),

"areas_for_improvement": feedback.get(

"areas_for_improvement",

[]

),

"recommendation": feedback.get(

"recommendation",

"Not enough information."

),

"total_questions": final_data.get("total_questions", 0),

}





def generate_scores_from_history(

qa_history: list,

position: str,

candidate_name: str

) -> dict:



# Kullanıcı hiç düzgün cevap vermediyse

if not has_meaningful_answers(qa_history):



return {

"radar": {

"Technical Competency": 2,

"Communication": 2,

"Problem Solving": 2,

"Experience Fit": 2,

"Motivation": 2,

},

"overall_comment": "The candidate did not provide enough meaningful answers.",

"strengths": [],

"areas_for_improvement": [

"Communication",

"Technical explanation",

"Interview participation"

],

"recommendation": "Not suitable based on insufficient responses.",

"total_questions": len(qa_history),

}



prompt = build_scoring_prompt(

qa_history,

position,

candidate_name

)



client = get_client()



response = client.chat.completions.create(

model="llama-3.3-70b-versatile",

messages=[{"role": "user", "content": prompt}],

temperature=0.1,

max_tokens=800,

)



clean = response.choices[0].message.content.strip()



clean = (

clean

.replace("```json", "")

.replace("```", "")

.strip()

)



try:

data = json.loads(clean)

return parse_final_scores(data, qa_history)



except json.JSONDecodeError:



return {

"error": "Scoring failed",

"raw": clean

} 