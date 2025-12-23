from .models import User,blog
from rest_framework import serializers
import re
from django.utils.text import slugify
from django.utils import timezone

class UserSerializers(serializers.ModelSerializer):
    cnfm_pass_code = serializers.CharField(write_only=True, required=True)
    class Meta:
        model=User
        fields=['id','email','first_name','last_name','password','cnfm_pass_code']
        extra_kwargs={'password':{'write_only':True},'cnfm_pass_code':{'write_only':True}} 

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*()_+=\-]", value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name should contain only letters.")
        if len(value) < 2:
            raise serializers.ValidationError("First name is too short.")
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name should contain only letters.")
        if len(value) < 2:
            raise serializers.ValidationError("Last name is too short.")
        return value
    def  validate(self,value):
        if value['password']!= value['cnfm_pass_code']:
            raise serializers.ValidationError({"confirm passcode":"The password doesn't match"})
        return value
    def create(self, validated_data):
        validated_data.pop('cnfm_pass_code')#removing the confirm pass code before saving
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
class ForgetPassword(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    security_code = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'security_code', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
 
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # remove it before creating
        user = User.objects.get(email=validated_data['email'])
        user.set_password(validated_data['password'])  # hash password
        user.security_code = 0  # clear security code after reset
        user.save()
        return user
class PostBlog(serializers.ModelSerializer):
    edit_it = serializers.BooleanField(write_only=True, required=False)
    delete_it=serializers.BooleanField(write_only=True,required=False)

    class Meta:
        model = blog
        fields = '__all__'
        read_only_fields = ['date_joined', 'user_id']

    def validate_blog_slug(self, value):
        return slugify(value)

    def create(self, validated_data):
        # Remove edit_it
        validated_data.pop('edit_it', None)
        validated_data.pop('delete_it', None)
        if not validated_data.get("blog_slug"):
            validated_data["blog_slug"] = slugify(validated_data["blog_title"])
        return blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # REMOVING THE NON DATABASE OBJECT
        #THESE EDIT IT AND DELETE IT ARE FLAGS NOT USED TO SAVE IN DATABASE
        validated_data.pop('edit_it', None)
        validated_data.pop('delete_it', None)
        if "blog_title" in validated_data and not validated_data.get("blog_slug"):
            validated_data["blog_slug"] = slugify(validated_data["blog_title"])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.last_edited = timezone.now()
        instance.save()
        return instance
    def delete(self,instance):

        instance.delete()
class searchBlogSerializer(serializers.ModelSerializer):
    user_first_name=serializers.CharField(source="user_id.first_name",read_only=True)
    user_last_name=serializers.CharField(source="user_id.last_name",read_only=True)
    class Meta:
        model=blog
        fields=['blog_title','blog_content','date_joined','user_first_name','user_last_name']