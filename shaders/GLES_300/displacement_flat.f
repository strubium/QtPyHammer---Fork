#version 300 es
layout(location = 0) out mediump vec4 outColour;

in mediump vec3 position;
in mediump float blend;
in mediump vec2 uv;
in mediump vec3 colour;

// uniform sampler2D blend_texture1; /* Move toward a Texture Atlas / Array */
// uniform sampler2D blend_texture2;

void main()
{
	mediump vec4 ambient = vec4(0.75, 0.75, 0.75, 1);
	mediump vec4 diffuse = vec4(1, 1, 1, 1) * blend;
	// mediump vec4 albedo1 = texture2D(blend_texture1, uv);
	// mediump vec4 albedo2 = texture2D(blend_texture2, uv);
	// mediump vec4 blend_albedo = mix(albedo1, albedo2, blend);

	outColour = vec4(colour, 1) * (ambient + diffuse);
	// outColour = vec4(uv.x, uv.y, 1, 1);
	// outColor = blend_albedo * (ambient + diffuse);
}
