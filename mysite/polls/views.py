from django.shortcuts import render, get_object_or_404

# Create your views here.
# from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.views import generic
from django.utils import timezone


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# ex: /polls/
class IndexView(generic.ListView):
    """ overwride default """
    template_name = 'polls/index.html' #汎用ビューは <app name>/<model name>_list.html 
    context_object_name = 'latest_question_list' #指定なし=question_list 

    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        # filter(pub_date__lte=timezone.now()) timezone.now 以前の Question を含んだクエリセットを返す



# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ','.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#     # template = loader.get_template('polls/index.html')
#     # context = {'latest_question_list': latest_question_list,}
#     # return HttpResponse(template.render(context, request))
#     context = {'latest_question_list': latest_question_list}
#    # return render(request, 'polls/index.html', context)

# Leave the rest of the views (detail, results, vote) unchanged

# ex: /polls/5/
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html' #DetailViewのtemplateは <app name>/<model name>_detail.html

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# def detail(request, question_id):
#     # return HttpResponse("You're looking at question %s." % question_id)
#     # q = Question.objects.get(pk=question_id)
#     # return HttpResponse(q)
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

# ex: /polls/5/results/
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html' #DetailViewの汎用templateは <app name>/<model name>_detail.html

# def results(request, question_id):
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})    

# ex: /polls/5/vote/
def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
