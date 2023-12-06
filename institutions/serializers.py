from rest_framework import serializers
from .models import Institution, Application


class ApplicationCreationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Application
        fields = (
            'content',
            'fee',
            'opening_date',
            'closing_date',
            'late_opening_date',
            'late_closing_date',
        )

    def validate(self, data):
        opening_date = data.get('opening_date')
        closing_date = data.get('closing_date')
        late_opening_date = data.get('late_opening_date')
        late_closing_date = data.get('late_closing_date')

        if opening_date and closing_date and opening_date >= closing_date:
            raise serializers.ValidationError("Opening date must be before Closing date.")
        
        
        if late_opening_date and late_closing_date and late_opening_date >= late_closing_date:
            raise serializers.ValidationError("Opening date must be before Closing date.")

        return data
    
class ApplicationSerializer(serializers.ModelSerializer):
    get_application_period = serializers.ReadOnlyField()
    get_late_application_period = serializers.ReadOnlyField()

    class Meta:
        model = Application
        fields = (
            'content',
            'fee',
            'get_application_period',
            'get_late_application_period',
        )

class InstitutionCreationSerializer(serializers.ModelSerializer):
    application = ApplicationCreationSerializer()

    class Meta:
        model = Institution
        fields = (
            'name',
            'abbreviation',
            'established_date',
            'website',
            'description',
            'content',
            # 'image',
            # 'raw_file',
            'Institution_type',
            'application',  # Include the serialized Application data
        )
    
    def create(self, validated_data):
        application_data = validated_data.pop('application')
        institution = Institution.objects.create(**validated_data)
        Application.objects.create(institution=institution, **application_data)
        return institution
    
    def update(self, instance, validated_data):
        # Update Institution fields
        for field in Institution._meta.fields:
            field_name = field.name
            if field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])

        # Update nested Application
        application_data = validated_data.get('application', {})
        application_instance = instance.application

        if application_instance:
            # If the Application instance already exists, update it
            for field in Application._meta.fields:
                field_name = field.name
                if field_name in application_data:
                    setattr(application_instance, field_name, application_data[field_name])

            application_instance.save()
        else:
            # If the Application instance doesn't exist, create it
            Application.objects.create(institution=instance, **application_data)

        instance.save()

        return instance

class InstitutionSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer()

    class Meta:
        model = Institution
        fields = (
            'id',
            'name',
            'abbreviation',
            'established_date',
            'website',
            'description',
            'content',
            # 'image',
            # 'raw_file',
            'Institution_type',
            'application',  # Include the serialized Application data
        )
    
    