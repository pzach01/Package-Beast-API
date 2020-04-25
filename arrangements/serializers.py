from rest_framework import serializers
from arrangements.models import Arrangement, BinLayout, BoxList
from django.utils.timezone import now
from arrangements.Box_Stuff_Python3_Only import box_stuff2 as optimize

from users.models import User
from users.serializers import UserSerializer

class BoxListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxList
        fields = ['height', 'width', 'length', 'volume', 'xCenter', 'yCenter', 'zCenter']

class BinLayoutSerializer(serializers.ModelSerializer):
    boxList = BoxListSerializer(many=True, read_only=True)

    class Meta:
        model = BinLayout
        fields = ['height', 'width', 'length', 'volume', 'cost', 'boxList']
        
class ArrangementSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    
    binLayout = BinLayoutSerializer(many=True, read_only=True)
    class Meta:
        model = Arrangement
        fields = ['id', 'owner', 'created', 'bins', 'boxes', 'binLayout']

    def create(self, validated_data):

        arrangement = Arrangement.objects.create(**validated_data)

        bins = validated_data.get('bins')
        boxes = validated_data.get('boxes')
        bins = bins.split(',')
        boxes = boxes.split(',')
        caluclated_bins=optimize.master_calculate_optimal_solution(bins,boxes)
     
        binDictionarys=[]
        for caluclated_bin in caluclated_bins:
            binDictionarys.append(caluclated_bin.to_dictionary())

        for binDictionary in binDictionarys:
            binDictionary.pop('id', None)
            boxLists = binDictionary.pop('boxList', None)
            binDictionary.pop('weightCapacity', None)
            binLayout = BinLayout.objects.create(arrangement=arrangement, **binDictionary)

            for boxList in boxLists:
                boxList.pop('weight', None)
                BoxList.objects.create(binLayout=binLayout, **boxList)
        return arrangement

    def update(self, instance, validated_data):
        instance.bins = validated_data.get('bins', instance.bins)
        instance.boxes = validated_data.get('boxes', instance.boxes)
        BinLayout.objects.filter(arrangement=instance).delete()
        bins = instance.bins.split(',')
        boxes = instance.boxes.split(',')


        calculated_bins=optimize.master_calculate_optimal_solution(bins,boxes)

        binDictionarys=[]
        for calculated_bins in calculated_bins:
            binDictionarys.append(calculated_bins.to_dictionary())

        for binDictionary in binDictionarys:
            binDictionary.pop('id', None)
            boxLists = binDictionary.pop('boxList', None)
            binDictionary.pop('weightCapacity', None)
            binLayout = BinLayout.objects.create(arrangement=instance, **binDictionary)

            for boxList in boxLists:
                boxList.pop('weight', None)
                BoxList.objects.create(binLayout=binLayout, **boxList)

        instance.save()
        return instance