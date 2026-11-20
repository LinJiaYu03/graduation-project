<template>
	<view class="form-card">
		<uni-forms ref="formRef" :modelValue="model" :rules="rules" label-position="top" label-width="auto">
			<uni-forms-item v-for="field in fields" :key="field.name" :label="field.label" :name="field.name" required>
				<input class="form-input" :password="!!field.password" :maxlength="field.maxlength || 20"
					:value="model[field.name]" :placeholder="field.placeholder" placeholder-style="color:#A39B90"
					@input="onInput(field.name, $event)" />
			</uni-forms-item>
		</uni-forms>

		<slot name="hint"></slot>

		<button class="form-submit" :loading="loading" :disabled="disabled || loading" @click="handleSubmit">
			{{ submitText }}
		</button>

		<slot></slot>
	</view>
</template>

<script setup>
	import {
		ref
	} from 'vue'

	const props = defineProps({
		model: {
			type: Object,
			required: true
		},
		fields: {
			type: Array,
			required: true
		},
		rules: {
			type: Object,
			required: true
		},
		submitText: {
			type: String,
			default: '提交'
		},
		loading: {
			type: Boolean,
			default: false
		},
		disabled: {
			type: Boolean,
			default: false
		}
	})

	const emit = defineEmits(['submit'])

	const formRef = ref(null)

	const onInput = (name, e) => {
		const value = e.detail ? e.detail.value : e.target.value
		props.model[name] = value
		if (formRef.value) {
			formRef.value.setValue(name, value)
		}
	}

	const handleSubmit = async () => {
		if (props.loading || props.disabled) return
		try {
			await formRef.value.validate()
		} catch (e) {
			return
		}
		emit('submit')
	}
</script>

<style lang="scss" scoped>
	.form-card {
		background: $bg-card;
		border: 1rpx solid $border-base;
		border-radius: $radius-md;
		padding: 56rpx 40rpx;
		box-shadow: $shadow-card;
	}

	.form-input {
		width: 100%;
		height: 88rpx;
		background: $bg-subtle;
		border-radius: $radius-sm;
		padding: 0 24rpx;
		font-size: 28rpx;
		color: $text-primary;
		box-sizing: border-box;
		border: 2rpx solid transparent;
	}

	.form-submit {
		width: 100%;
		height: 88rpx;
		background: $brand-primary;
		border-radius: $radius-pill;
		color: $text-on-primary;
		font-size: 30rpx;
		font-weight: 500;
		margin-top: 40rpx;
		border: none;
		display: flex;
		align-items: center;
		justify-content: center;

		&::after {
			border: none;
		}

		&:active {
			background: $brand-primary-deep;
		}

		&[disabled] {
			opacity: 0.6;
			background: $brand-primary;
		}
	}
</style>
