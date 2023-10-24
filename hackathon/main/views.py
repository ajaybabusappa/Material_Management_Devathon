from django.shortcuts import render
from .models import courses,studentcourse,teachercourse,file,student,teacher
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView  ,DetailView, UpdateView ,DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
# Create your views here.
#request.session['student_id']='831727'



from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission

permission =  GoogleDriveFilePermission(
   GoogleDrivePermissionRole.READER,
   GoogleDrivePermissionType.USER,
   
)



@csrf_exempt
def mainpage(request):
	return render(request,'buttons.html')

@csrf_exempt
def studentsavreq(request):
	return render(request,'Student_Registration.html')

@csrf_exempt
def teachersavreq(request):
	return render(request,'Faculty_Registration.html')


@csrf_exempt
def studentsave(request):
	if request.method == 'POST':
		fullname=request.POST['full_name']
		email=request.POST['email']
		password=request.POST['password']
		
		department_id=request.POST['department_id']
		student_id=request.POST['student_id']
		phonenumber=request.POST['phone']
		students=student.objects.create(full_name=fullname,mailid=email,password=password, phonenumber=phonenumber, department_id=department_id, student_id=student_id)
		courses_list= courses.objects.all()
		for i in courses_list:
			print(i.course_id)
		request.session['student_id']=student_id
		request.session['teacher']=False;
		return render(request,'select_course.html',{'courses_list':courses_list})
	else:
		return render(request,'index.html')



@csrf_exempt
def teachersave(request):
	if request.method == 'POST':
		fullname=request.POST['full_name']
		email=request.POST['email']
		password=request.POST['password']
		phonenumber=request.POST['phone']
		department_id=request.POST['department_id']
		teacher_id=request.POST['teacher_id']
		student=teacher.objects.create(full_name=fullname,mailid=email,password=password, phonenumber=phonenumber, department_id=department_id, teacher_id=teacher_id)

		courses_list= courses.objects.all()


		for i in courses_list:
			print(i.course_id)
		request.session['student_id']=teacher_id
		request.session['teacher']=True;
		return render(request,'select_course.html',{'courses_list':courses_list})

	else:
		return render(request,'errorpage.html')




def showloginpage(request):
	return render(request,'Material_Management_Portal.html')


@csrf_exempt
def studentlogin(request):
	if request.method=='POST':
		student_id= request.POST['student_id']
		password = request.POST['password']
		studentx = student.objects.filter(student_id=student_id , password=password)
		request.session['student_id']=student_id
		if studentx:
			contacx=studentcourse.objects.filter(student_id=student_id)
			for i in contacx:
				x=courses.objects.filter(course_id=i.course_id)
			request.session['teacher']=False;
			request.session['student']=True;
			return render(request,'courses.html',{'courses_list':x,'session':request.session['teacher']})
		else:
			message="wrong creds"
			return render(request,'errorpage.html',{'message': message})

	else:
		if request.session['student']:
			
			contacx=studentcourse.objects.filter(student_id=request.session['student_id'])
			for i in contacx:
				x=courses.objects.filter(course_id=i.course_id)
				request.session['student']=True;
			return render(request,'courses.html',{'courses_list':x,'session':request.session['teacher']})



@csrf_exempt
def teacherlogin(request):
	if request.method=='POST':
		student_id= request.POST['student_id']
		password = request.POST['password']
		studentx = teacher.objects.filter(teacher_id=student_id , password=password)
		request.session['student_id']=student_id


		if studentx:
			contacx=studentcourse.objects.filter(student_id=student_id)

			for i in contacx:
				x=courses.objects.filter(course_id=i.course_id)
			request.session['teacher']=True;
			return render(request,'courses.html',{'courses_list':x,'session':request.session['teacher']})
		else:


			message="wrong creds"
			return render(request,'errorpage.html',{'message': message})
	else:
		
		if request.session['teacher']:
			
			contacx=studentcourse.objects.filter(student_id=request.session['student_id'])
			for i in contacx:
				x=courses.objects.filter(course_id=i.course_id)
				request.session['teacher']=True;
			return render(request,'courses.html',{'courses_list':x,'session':request.session['teacher']})

	



@csrf_exempt
def courseslist(request):
	print('ahdka')
	if request.method=='POST':
		courses_list1 = request.POST.getlist('course')
		for i in courses_list1:
			studentcourse.objects.create(course_id=i,student_id=request.session['student_id'])
			print("sdns")
		return HttpResponseRedirect('/')
	else:
		return render(request,'errorpage.html')



def postfile(request):
	if request.session['teacher']:
		x=studentcourse.objects.filter(student_id=request.session['student_id'])

		return render(request,'Uploading_portal.html',{'x':x})
	else:
		return render(request,'errorpage.html')



def viewfiles(request):
	x = studentcourse.objects.filter(student_id=request.session['student_id'])
	filesto1=[]
	for i in x:
		filesto=file.objects.filter(course_id=i.course_id)
		for t in filesto:
			filesto1.append(t)

	return render(request,'allfiles1.html',{'files':filesto1,'session':request.session['teacher'],'x':x})



@csrf_exempt
def upload(request):
	doc=request.FILES
	file_pdf = doc['file']
	filename=request.POST['filename']
	file_description = request.POST['description']
	course_id=request.POST[course_id]
	files=file.objects.create(map_name=filename,map_data=file_pdf,descreption=file_description,course_id=course_id)
	print(file_pdf)
	print(filename)
	return render(request,'index.html')




class Deletepostviewjob(DeleteView):
	model = file
	template_name = 'delete_post.html'
	success_url = reverse_lazy('viewfiles')





@csrf_exempt
def listfiles (request):
	doc=request.FILES
	file_pdf = doc['file']
	filename=request.POST['filename']
	file_description = request.POST['description']
	course_id1=request.POST['course_id']
	files=file.objects.create(map_name=filename,map_data=file_pdf,descreption=file_description,course_id=course_id1)
	print(file_pdf)
	print(filename)
	return HttpResponseRedirect('/teacher/loggedin/')



	#x = studentcourse.objects.filter(student_id=request.session['student_id'])
	#filesto1=[]
	#for i in x:
	#	filesto=file.objects.filter(course_id=i.course_id)
	#	for t in filesto:
	#		filesto1.append(t)


	#return render(request,'allfiles1.html',{'files':filesto1,'session':request.session['teacher'],'x':x})






@csrf_exempt
def search(request):
	course = request.POST['course']
	filesto = file.objects.filter(course_id=course)
	return render(request,'searched_files.html',{'files':filesto,'session':request.session['teacher']})
