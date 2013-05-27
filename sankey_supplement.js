
function auto_y(node, maxes, sort_order, pad)
{

	var y_coord = 0;
		name = node.name.slice(2);
		group_start = -1 * pad;

	for (c = 0 ; c <= sort_order.indexOf(name); c++)
	{
		group_start = group_start + pad + maxes[sort_order[c]];
	}


	y_coord = group_start - node.dy;

	if (sort_order.indexOf(name) % 2 == 1)
	{
		y_coord = group_start - node.dy - maxes[name] + node.dy;
	}

	return y_coord;
}



function find_max(maxes, n)
{
	//	maxes = an object that holds max values
	//	n = node object

	var name = n.name.slice(2);				//	group

	//	default case... no value exists yet
	if (typeof(maxes[name]) == 'undefined')
	{
		maxes[name] = 0;
	}

	// console.log(name, n.dy, maxes[name]);
	//	check to see which is bigger: the stored value or this guy's
	if (n.dy >= maxes[name])
	{
		maxes[name] = n.dy;
	}

	return maxes;
}


function find_max_terms(mt, n)
{
	//	mt = an object that holds max terms for a given group
	//	n = node object

	var name = n.name.slice(2);				//	group
		term = n.name.slice(0, 2);			//	term

	//	default case... no value exists yet
	if (typeof(mt[name]) == 'undefined')
	{
		mt[name] = 0;
	}

	// console.log(name, n.dy, mt[name]);
	//	check to see which is bigger: the stored value or this guy's
	if (term >= mt[name])
	{
		mt[name] = term;
	}

	return mt;
}


function calculate_legend_x (n, nw, width)
{
	// n = node, nw = node_width, width = chart width

	var output = 6 + nw;

	if (n.x + nw < width)
		output = output + (width - n.x - nw);

	return output;
}


function write_legend(n, mt)
{
	// n is a node, mt = object with max terms for given groups

	var name = n.name;
		output = "";
		this_semester = name.slice(0, 2);

	if (mt[name.slice(2)] == this_semester)
	{
		switch(name.slice(2))
		{
			//	generic
			case 'ECE':
			{				
				output = "ECE";
				break;
			}			
			case 'ME ':
			{				
				output = "ME";
				break;
			}			
			case 'E  ':
			{				
				output = "E";
				break;
			}			
			case 'U  ':
			{				
				output = "Undeclared";
				break;
			}			
			case 'LOA':
			{				
				output = "On LOA";
				break;
			}

			// just women 
			case 'ECEF':
			{				
				output = "Female ECE";
				break;
			}			
			case 'ME F':
			{				
				output = "Female ME";
				break;
			}			
			case 'E  F':
			{				
				output = "Female E";
				break;
			}			
			case 'U  F':
			{				
				output = "Female Undeclared";
				break;
			}			
			case 'LOAF':
			{				
				output = "Female on LOA";
				break;
			}

			//	just men
			case 'ECEM':
			{				
				output = "Male ECE";
				break;
			}			
			case 'ME M':
			{				
				output = "Male ME";
				break;
			}			
			case 'E  M':
			{				
				output = "Male E";
				break;
			}			
			case 'U  M':
			{				
				output = "Male Undeclared";
				break;
			}			
			case 'LOAM':
			{				
				output = "Male on LOA";
				break;
			}
		}
	}
	return output;
}


function choose_color(n)
{	
	var name = n.slice(2);
	var output = '#ffbb78' //beige. 

	// '#ab1267'				//	magenta
	// 	output = '#1f77b4';		//	blue	
	// 	output = '#2ca02c';		//	green	
	// 	output = '#ff7f0e'		//	orange
	// 	 '#5625ad'				//	swanky purple
	// 	output = '#455515';	
	// 	output = '#ffbb78';		//	beige
	//'#dd4010';	//	blood orange
	//'#ff7f0e';		//	classic orange
	// output = '#dd2020';		//	nice red

	switch (name.slice(0, 3))
	{
		case 'ECE':
			{
				output = '#dd2020';		//	nice red
				break;
			}

		case 'E  ':
			{
				output = '#2ca02c';		//	green
				break;
			}

		case 'U  ':
			{
				output = '#5625ad'		//	swanky purple
				break;
			}

		case 'ME ':
			{
				output = '#1f77b4';		//	blue
				break;
			}

		// case 'GRX':
		// 	{
		// 		output = '#455515';
		// 		break;
		// 	}

		// case 'TOL':
		// 	{
		// 		output = '#ffbb78';		//	classic beige
		// 		break;
		// 	}

		// case 'TOX':
		// 	{
		// 		output = '#dd9945';
		// 		break;
		// 	}

		// case 'TOE':
		// 	{
		// 		output = '#ffbb78';
		// 		break;
		// 	}

		default://case 'TOL':
			{
				output = '#ffbb78';
				break;
			}
	}

	if (name.slice(4, 5) == 'F')
	{
		var temp = output.slice(1);
		output = '#'
		// we need to lighten the color
		for (i = 0; i < 3; i++)
		{
			start_color = parseInt(temp.slice(i * 2, i * 2 + 2), 16);
			lighter_color = (start_color * 0.8).toString(16);
			output += lighter_color;
		}
		console.log(['lighter now: ', output])
	}

	return output;
}